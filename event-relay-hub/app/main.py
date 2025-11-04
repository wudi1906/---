"""
Event Relay Hub 主应用
"""
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, Request, Depends, Query, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, or_

from app.settings import settings
from app.models import (
    init_db,
    get_db,
    Event,
    EventResponse,
    EventStats,
    ReplayResponse,
    PaginatedEvents,
    PaginatedDeadLetters,
    BulkReplayRequest,
    BulkReplayResult,
    ForwardLog,
    SignatureTemplateSchema,
    SignatureTemplateUpdate,
    DeadLetterSchema,
    DeadLetterEvent,
)
from app.webhooks import WebhookHandler
from app.forwarder import EventForwarder
from app.rate_limiter import limiter
try:
    from slowapi.errors import RateLimitExceeded  # type: ignore
    from slowapi.middleware import SlowAPIMiddleware  # type: ignore
    _slowapi_available = True
except ImportError:  # pragma: no cover - 测试环境降级
    RateLimitExceeded = Exception  # type: ignore

    class SlowAPIMiddleware:  # type: ignore
        """空实现，使应用在 slowapi 缺失时也能启动"""

        def __init__(self, app) -> None:  # noqa: D401
            self.app = app

        async def __call__(self, scope, receive, send):
            await self.app(scope, receive, send)

    _slowapi_available = False
import random
import json
from pathlib import Path

from app.signature_service import SignatureService
from pydantic import BaseModel
# --- Signature test models ---
class SignatureTestRequest(BaseModel):
    payload: Optional[Dict] = None
    timestamp: Optional[int] = None


class SignatureTestResponse(BaseModel):
    header: str
    value: str
    example_curl: Optional[str] = None



# 创建应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="通用 Webhook 事件汇聚与转发中台",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.state.limiter = limiter
if _slowapi_available:
    app.add_middleware(SlowAPIMiddleware)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件
try:
    app.mount("/static", StaticFiles(directory="frontend"), name="static")
except Exception:  # frontend 目录可能不存在
    pass

app.mount(
    "/i18n",
    StaticFiles(directory=str(Path(__file__).resolve().parent / "i18n")),
    name="i18n",
)


def parse_iso_datetime(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid datetime format, expected ISO 8601") from exc


@app.on_event("startup")
async def startup_event():
    """启动时初始化"""
    init_db()
    print(f"✓ {settings.APP_NAME} v{settings.APP_VERSION} 启动成功")
    print(f"  - 监听地址: http://{settings.HOST}:{settings.PORT}")
    print(f"  - API文档: http://{settings.HOST}:{settings.PORT}/api/docs")


if _slowapi_available:

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        """速率限制异常处理"""
        return {
            "error": "Rate limit exceeded",
            "detail": str(exc)
        }


def _detect_language(request: Request) -> str:
    cookie_lang = request.cookies.get("portfolio_lang")
    if cookie_lang and cookie_lang in {"en", "zh"}:
        return cookie_lang
    header_lang = (request.headers.get("Accept-Language") or "").lower()
    if header_lang.startswith("zh"):
        return "zh"
    return "en"


def _render_home(lang: str) -> str:
    data_path = Path(__file__).resolve().parent / "i18n" / f"p2.{lang}.json"
    fallback_path = Path(__file__).resolve().parent / "i18n" / "p2.en.json"
    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
    except Exception:
        data = json.loads(fallback_path.read_text(encoding="utf-8"))

    features_html = ''.join(
        f"""<div class='feature-card'><h3>{item['title']}</h3><p>{item['desc']}</p></div>"""
        for item in data['features']
    )
    endpoints_html = ''.join(f"<code>{line}</code>" for line in data['endpoints']['items'])

    return f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Event Relay Hub</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #6366f1 0%, #7c3aed 100%);
                min-height: 100vh;
                padding: 40px 20px;
                color: white;
            }}
            .container {{ max-width: 1000px; margin: 0 auto; }}
            .lang-switcher {{
                position: fixed;
                top: 24px;
                right: 24px;
                display: flex;
                flex-direction: column;
                align-items: flex-end;
                gap: 6px;
            }}
            .lang-toggle {{
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 8px 16px;
                border-radius: 999px;
                border: 1px solid rgba(148, 163, 184, 0.35);
                background: rgba(15, 23, 42, 0.6);
                color: #e2e8f0;
                font-weight: 600;
                cursor: pointer;
            }}
            .lang-options {{
                display: none;
                flex-direction: column;
                border-radius: 14px;
                border: 1px solid rgba(148, 163, 184, 0.35);
                background: rgba(15, 23, 42, 0.85);
                backdrop-filter: blur(16px);
                overflow: hidden;
            }}
            .lang-options.open {{ display: flex; }}
            .lang-option {{
                padding: 10px 16px;
                color: #e2e8f0;
                font-size: 0.9rem;
                text-align: left;
                border: none;
                background: transparent;
                cursor: pointer;
            }}
            .lang-option:hover,
            .lang-option:focus-visible,
            .lang-option.active {{
                background: rgba(96, 165, 250, 0.35);
                outline: none;
            }}
            .hero {{ text-align: center; margin-bottom: 60px; }}
            h1 {{ font-size: 3rem; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }}
            .subtitle {{ font-size: 1.25rem; margin-bottom: 2rem; opacity: 0.95; max-width: 700px; margin-left: auto; margin-right: auto; line-height: 1.6; }}
            .features {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 20px;
                margin: 40px 0;
            }}
            .feature-card {{
                background: rgba(255,255,255,0.18);
                padding: 24px;
                border-radius: 14px;
                backdrop-filter: blur(12px);
                border: 1px solid rgba(255,255,255,0.25);
            }}
            .cta-buttons {{ display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; margin: 40px 0; }}
            .btn {{
                padding: 14px 32px;
                background: rgba(255,255,255,0.15);
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-weight: 600;
                transition: all 0.2s;
                border: 1px solid rgba(255,255,255,0.3);
                display: inline-flex;
                align-items: center;
                gap: 8px;
            }}
            .btn:hover {{ transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0,0,0,0.2); }}
            .endpoints {{
                background: rgba(255,255,255,0.12);
                padding: 32px;
                border-radius: 14px;
                backdrop-filter: blur(12px);
                margin-top: 40px;
            }}
            .endpoints h3 {{ margin-bottom: 16px; font-size: 1.3rem; }}
            .endpoints code {{
                display: block;
                background: rgba(0,0,0,0.25);
                padding: 10px 16px;
                border-radius: 8px;
                margin: 10px 0;
                font-family: 'Courier New', monospace;
                font-size: 0.95rem;
            }}
        </style>
    </head>
    <body>
        <div class="lang-switcher" role="navigation" aria-label="Language selector">
            <button id="langToggle" class="lang-toggle" type="button" aria-expanded="false">
                <span>🌐</span><span data-i18n="lang.toggle">{data['lang']['toggle']}</span>
            </button>
            <div id="langOptions" class="lang-options" role="menu">
                <button class="lang-option" data-lang="en" role="menuitemradio" aria-checked="{str(lang=='en').lower()}">{data['lang']['options']['en']}</button>
                <button class="lang-option" data-lang="zh" role="menuitemradio" aria-checked="{str(lang=='zh').lower()}">{data['lang']['options']['zh']}</button>
            </div>
        </div>
        <div class="container">
            <div class="hero">
                <h1 data-i18n="hero.title">{data['hero']['title']}</h1>
                <p class="subtitle" data-i18n="hero.subtitle">{data['hero']['subtitle']}</p>
            </div>
            <div class="features" id="features">{features_html}</div>
            <div class="cta-buttons">
                <a href="/api/docs" class="btn" data-i18n="hero.cta.docs">{data['hero']['cta']['docs']}</a>
                <a href="/console/events" class="btn" data-i18n="hero.cta.console">{data['hero']['cta']['console']}</a>
                <button onclick="seedDemo()" class="btn" data-i18n="hero.cta.import">{data['hero']['cta']['import']}</button>
                <button onclick="resetDemo()" class="btn" data-i18n="hero.cta.reset">{data['hero']['cta']['reset']}</button>
            </div>
            <div class="endpoints">
                <h3 data-i18n="endpoints.title">{data['endpoints']['title']}</h3>
                {endpoints_html}
            </div>
        </div>
        <script>
            const LANG_STORAGE_KEY = 'portfolio-lang';
            const SUPPORTED_LANGS = ['en', 'zh'];
            let currentLang = '{lang}';

            async function fetchTranslations(lang) {{
                const res = await fetch(`/i18n/p2.${{lang}}.json`, {{ cache: 'no-cache' }});
                if (!res.ok) throw new Error('Failed to fetch translations');
                return res.json();
            }}

            const ALERT_TEXT = {{
                importSuccess: "{data['alerts']['importSuccess']}",
                importFailed: "{data['alerts']['importFailed']}",
                resetSuccess: "{data['alerts']['resetSuccess']}",
                resetFailed: "{data['alerts']['resetFailed']}"
            }};

            function applyTranslations(data) {{
                document.querySelector('[data-i18n="hero.title"]').textContent = data.hero.title;
                document.querySelector('[data-i18n="hero.subtitle"]').textContent = data.hero.subtitle;
                document.querySelector('[data-i18n="hero.cta.docs"]').textContent = data.hero.cta.docs;
                document.querySelector('[data-i18n="hero.cta.console"]').textContent = data.hero.cta.console;
                document.querySelector('[data-i18n="hero.cta.import"]').textContent = data.hero.cta.import;
                document.querySelector('[data-i18n="hero.cta.reset"]').textContent = data.hero.cta.reset;
                document.querySelector('[data-i18n="endpoints.title"]').textContent = data.endpoints.title;
                const features = document.getElementById('features');
                features.innerHTML = data.features.map(item => `<div class="feature-card"><h3>${{item.title}}</h3><p>${{item.desc}}</p></div>`).join('');
                const endpoints = data.endpoints.items.map(line => `<code>${{line}}</code>`).join('');
                document.querySelector('.endpoints').innerHTML = `<h3 data-i18n="endpoints.title">${{data.endpoints.title}}</h3>${{endpoints}}`;
                updateLangButtons(data);
            }}

            function updateLangButtons(data) {{
                document.querySelector('[data-i18n="lang.toggle"]').textContent = data.lang.toggle;
                document.querySelectorAll('#langOptions .lang-option').forEach(btn => {{
                    const lang = btn.getAttribute('data-lang');
                    btn.textContent = data.lang.options[lang];
                    const isActive = lang === currentLang;
                    btn.classList.toggle('active', isActive);
                    btn.setAttribute('aria-checked', isActive ? 'true' : 'false');
                }});
            }}

            async function changeLanguage(lang) {{
                if (!SUPPORTED_LANGS.includes(lang)) lang = 'en';
                const data = await fetchTranslations(lang);
                currentLang = lang;
                localStorage.setItem(LANG_STORAGE_KEY, lang);
                document.cookie = `portfolio_lang=${{lang}}; path=/; max-age=${{60*60*24*365}}`;
                document.documentElement.setAttribute('lang', lang === 'zh' ? 'zh-CN' : 'en');
                applyTranslations(data);
            }}

            const savedLang = localStorage.getItem(LANG_STORAGE_KEY);
            const initialLang = savedLang && SUPPORTED_LANGS.includes(savedLang) ? savedLang : '{lang}';
            if (initialLang !== currentLang) {{
                changeLanguage(initialLang);
            }} else {{
                fetchTranslations(currentLang).then(applyTranslations).catch(console.error);
            }}

            const langToggle = document.getElementById('langToggle');
            const langOptions = document.getElementById('langOptions');
            langToggle.addEventListener('click', () => {{
                const isOpen = langOptions.classList.toggle('open');
                langToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
            }});
            langOptions.addEventListener('click', (event) => {{
                if (event.target.matches('.lang-option')) {{
                    langOptions.classList.remove('open');
                    langToggle.setAttribute('aria-expanded', 'false');
                    changeLanguage(event.target.dataset.lang);
                }}
            }});
            document.addEventListener('click', (event) => {{
                if (!langOptions.contains(event.target) && event.target !== langToggle) {{
                    langOptions.classList.remove('open');
                    langToggle.setAttribute('aria-expanded', 'false');
                }}
            }});

            window.addEventListener('storage', (event) => {{
                if (event.key === LANG_STORAGE_KEY && event.newValue && event.newValue !== currentLang) {{
                    changeLanguage(event.newValue);
                }}
            }});

            async function seedDemo() {{
                try {{
                    const res = await fetch('/api/demo/seed', {{ method: 'POST' }});
                    const data = await res.json();
                    if (data.success) {{
                        alert(ALERT_TEXT.importSuccess);
                    }} else {{
                        const detail = data.error || 'Unknown error';
                        alert(ALERT_TEXT.importFailed.replace('{{error}}', detail));
                    }}
                }} catch (error) {{
                    const detail = (error && error.message) ? error.message : 'Unknown error';
                    alert(ALERT_TEXT.importFailed.replace('{{error}}', detail));
                }}
            }}

            async function resetDemo() {{
                if (!confirm('{data['alerts']['resetConfirm']}')) return;
                try {{
                    const res = await fetch('/api/demo/reset', {{ method: 'POST' }});
                    const dataResp = await res.json();
                    if (dataResp.success) {{
                        alert(ALERT_TEXT.resetSuccess);
                    }} else {{
                        const detail = dataResp.error || 'Unknown error';
                        alert(ALERT_TEXT.resetFailed.replace('{{error}}', detail));
                    }}
                }} catch (error) {{
                    const detail = (error && error.message) ? error.message : 'Unknown error';
                    alert(ALERT_TEXT.resetFailed.replace('{{error}}', detail));
                }}
            }}

            window.seedDemo = seedDemo;
            window.resetDemo = resetDemo;
        </script>
    </body>
    </html>
    """


@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    """双语营销首页"""
    lang = _detect_language(request)
    return HTMLResponse(_render_home(lang))


@app.get("/console/events", response_class=HTMLResponse)
async def events_console():
    template_path = Path(__file__).resolve().parent / "templates" / "events_console.html"
    if template_path.exists():
        return template_path.read_text(encoding="utf-8")
    return HTMLResponse("<h1>Console template missing</h1>", status_code=404)


@app.get("/console/signatures", response_class=HTMLResponse)
async def signatures_console():
    template_path = Path(__file__).resolve().parent / "templates" / "signature_settings.html"
    if template_path.exists():
        return template_path.read_text(encoding="utf-8")
    return HTMLResponse("<h1>Signature settings template missing</h1>", status_code=404)


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/webhook/github")
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def github_webhook(request: Request, db: Session = Depends(get_db)):
    """接收 GitHub Webhook"""
    handler = WebhookHandler(db)
    return await handler.handle_github(request)


@app.post("/webhook/stripe")
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """接收 Stripe Webhook"""
    handler = WebhookHandler(db)
    return await handler.handle_stripe(request)


@app.post("/webhook/custom")
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def custom_webhook(request: Request, db: Session = Depends(get_db)):
    """接收自定义 Webhook"""
    handler = WebhookHandler(db)
    return await handler.handle_custom(request)


def get_last_forward_log(
    db: Session,
    event_id: int,
    target_url: Optional[str] = None,
    success_only: bool = False,
):
    query = db.query(ForwardLog).filter(ForwardLog.event_id == event_id)
    if target_url:
        query = query.filter(ForwardLog.target_url == target_url)
    if success_only:
        query = query.filter(ForwardLog.success == True)
    return query.order_by(desc(ForwardLog.created_at)).first()


def evaluate_replay_guard(db: Session, event_id: int, target_url: str) -> Optional[Dict[str, Any]]:
    now = datetime.utcnow()
    cooldown = max(settings.REPLAY_COOLDOWN_SECONDS, 0)
    success_ttl = max(settings.REPLAY_SUCCESS_TTL_SECONDS, 0)

    if success_ttl:
        last_success = get_last_forward_log(db, event_id, target_url, success_only=True)
        if last_success and last_success.created_at:
            diff = (now - last_success.created_at).total_seconds()
            if diff < success_ttl:
                elapsed = max(int(diff), 0)
                remaining = max(int(success_ttl - diff), 0)
                return {
                    "action": "skip_success",
                    "message": f"事件 #{event_id} 在 {elapsed} 秒前已成功转发，跳过重复操作。",
                    "note": f"最近 {elapsed} 秒内已成功转发",
                    "last_success_at": last_success.created_at,
                    "remaining": remaining,
                }

    if cooldown:
        last_attempt = get_last_forward_log(db, event_id, target_url, success_only=False)
        if last_attempt and last_attempt.created_at:
            diff = (now - last_attempt.created_at).total_seconds()
            if diff < cooldown:
                remaining = max(int(cooldown - diff), 1)
                return {
                    "action": "cooldown",
                    "message": f"事件 #{event_id} 正在冷却，还需 {remaining} 秒。",
                    "retry_after": remaining,
                    "last_attempt_at": last_attempt.created_at,
                }

    return None


@app.get("/api/events/search", response_model=PaginatedEvents)
async def search_events(
    source: Optional[str] = Query(None, description="事件源"),
    event_type: Optional[str] = Query(None, description="事件类型"),
    signature_valid: Optional[bool] = Query(None, description="签名是否有效"),
    start_time: Optional[str] = Query(None, description="起始时间，ISO8601"),
    end_time: Optional[str] = Query(None, description="结束时间，ISO8601"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=200, description="每页数量"),
    db: Session = Depends(get_db),
):
    query = db.query(Event)

    if source:
        query = query.filter(Event.source == source)
    if event_type:
        query = query.filter(Event.event_type == event_type)
    if signature_valid is not None:
        query = query.filter(Event.signature_valid == signature_valid)

    start_dt = parse_iso_datetime(start_time)
    end_dt = parse_iso_datetime(end_time)

    if start_dt:
        query = query.filter(Event.created_at >= start_dt)
    if end_dt:
        query = query.filter(Event.created_at <= end_dt)

    total = query.count()
    items = (
        query.order_by(desc(Event.created_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return PaginatedEvents(total=total, page=page, page_size=page_size, items=items)


@app.get("/api/events", response_model=List[EventResponse])
async def get_events(
    source: Optional[str] = Query(None, description="事件源"),
    event_type: Optional[str] = Query(None, description="事件类型"),
    days: int = Query(7, ge=1, le=90, description="查询天数"),
    limit: int = Query(100, ge=1, le=1000, description="返回数量"),
    db: Session = Depends(get_db)
):
    """获取事件列表"""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    query = db.query(Event).filter(Event.created_at >= cutoff_date)
    
    if source:
        query = query.filter(Event.source == source)
    if event_type:
        query = query.filter(Event.event_type == event_type)
    
    events = query.order_by(desc(Event.created_at)).limit(limit).all()
    return events


@app.get("/api/events/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """获取单个事件详情"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@app.post("/api/events/{event_id}/replay", response_model=ReplayResponse)
async def replay_event(
    event_id: int,
    target_url: Optional[str] = Query(None, description="目标URL"),
    db: Session = Depends(get_db)
):
    """重放事件"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    forwarder = EventForwarder()
    url = target_url or settings.FORWARD_URL
    
    if not url:
        raise HTTPException(status_code=400, detail="No target URL provided")
    guard = evaluate_replay_guard(db, event_id, url)
    if guard:
        if guard.get("action") == "skip_success":
            return ReplayResponse(
                success=True,
                message=guard["message"],
                event_id=event_id,
                last_success_at=guard.get("last_success_at"),
                notes=guard.get("note"),
            )
        if guard.get("action") == "cooldown":
            return ReplayResponse(
                success=False,
                message=guard["message"],
                event_id=event_id,
                retry_after=guard.get("retry_after"),
                last_attempt_at=guard.get("last_attempt_at"),
            )
    
    success = await forwarder.replay_event(event_id, url)

    response = ReplayResponse(
        success=success,
        message="事件重放成功" if success else "重放失败",
        event_id=event_id,
    )
    if success:
        response.last_success_at = datetime.utcnow()
    else:
        response.last_attempt_at = datetime.utcnow()
    return response


@app.post("/api/events/replay/batch", response_model=BulkReplayResult)
async def replay_events_batch(payload: BulkReplayRequest, db: Session = Depends(get_db)):
    """批量重放事件"""

    forwarder = EventForwarder()
    success_ids: List[int] = []
    failed: Dict[int, str] = {}
    notes: Dict[int, str] = {}

    seen = set()
    unique_ids: List[int] = []
    for event_id in payload.ids:
        if event_id in seen:
            failed[event_id] = "Duplicate id ignored"
            continue
        seen.add(event_id)
        unique_ids.append(event_id)
    for event_id in unique_ids:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            failed[event_id] = "Event not found"
            continue

        target = payload.target_url or settings.FORWARD_URL
        if not target:
            failed[event_id] = "No target URL provided"
            continue

        guard = evaluate_replay_guard(db, event_id, target)
        if guard:
            if guard.get("action") == "skip_success":
                success_ids.append(event_id)
                notes[event_id] = guard["message"]
                continue
            if guard.get("action") == "cooldown":
                failed[event_id] = guard["message"]
                continue

        success = await forwarder.replay_event(event_id, target)
        if success:
            success_ids.append(event_id)
        else:
            failed[event_id] = "Replay failed"

    return BulkReplayResult(success_ids=success_ids, failed=failed, notes=notes)


@app.get("/api/stats", response_model=EventStats)
async def get_stats(db: Session = Depends(get_db)):
    """获取事件统计"""
    total = db.query(func.count(Event.id)).scalar()
    
    # 按来源统计
    by_source = {}
    for source, count in db.query(Event.source, func.count(Event.id)).group_by(Event.source).all():
        by_source[source] = count
    
    # 按事件类型统计
    by_event_type = {}
    for event_type, count in db.query(Event.event_type, func.count(Event.id)).group_by(Event.event_type).limit(10).all():
        if event_type:
            by_event_type[event_type] = count
    
    # 最近24小时
    cutoff = datetime.utcnow() - timedelta(hours=24)
    recent_24h = db.query(func.count(Event.id)).filter(Event.created_at >= cutoff).scalar()
    
    # 签名成功率
    total_with_sig = db.query(func.count(Event.id)).scalar()
    valid_sig = db.query(func.count(Event.id)).filter(Event.signature_valid == True).scalar()
    sig_success_rate = (valid_sig / total_with_sig * 100) if total_with_sig > 0 else 0.0

    forward_success = db.query(func.count(ForwardLog.id)).filter(ForwardLog.success == True).scalar() or 0
    forward_failed = db.query(func.count(ForwardLog.id)).filter(ForwardLog.success == False).scalar() or 0
    dead_letters = db.query(func.count(DeadLetterEvent.id)).scalar() or 0
    
    return EventStats(
        total_events=total,
        by_source=by_source,
        by_event_type=by_event_type,
        recent_24h=recent_24h,
        signature_success_rate=sig_success_rate,
        forward_success=forward_success,
        forward_failed=forward_failed,
        dead_letters=dead_letters,
    )


@app.post("/api/demo/seed")
async def demo_seed(db: Session = Depends(get_db)):
    """导入示例事件数据"""
    sources = ["stripe", "github", "slack"]
    event_types_map = {
        "stripe": ["payment.succeeded", "subscription.created", "invoice.paid"],
        "github": ["push", "pull_request", "issue_comment"],
        "slack": ["message.im", "app_mention", "reaction_added"]
    }
    
    created_count = 0
    for days_ago in range(7, 0, -1):
        for source in sources:
            for event_type in random.sample(event_types_map[source], k=random.randint(1, 3)):
                event = Event(
                    source=source,
                    event_type=event_type,
                    payload=json.dumps({"id": f"evt_{random.randint(1000,9999)}", "data": "sample"}),
                    headers=json.dumps({"X-Source": source.title()}),
                    signature_valid=random.choice([True, True, True, False]),
                    created_at=datetime.utcnow() - timedelta(days=days_ago, hours=random.randint(0, 23))
                )
                db.add(event)
                created_count += 1
                
                # 添加转发日志
                if random.random() > 0.3:
                    log = ForwardLog(
                        event_id=None,  # 稍后会关联
                        target_url="https://api.example.com/webhook",
                        status_code=random.choice([200, 200, 200, 500]),
                        success=random.choice([True, True, True, False]),
                        created_at=event.created_at
                    )
                    db.add(log)
    
    db.commit()
    return {"success": True, "seeded_events": created_count}


@app.post("/api/demo/reset")
async def demo_reset(db: Session = Depends(get_db)):
    """清空所有事件数据"""
    db.query(Event).delete()
    db.query(ForwardLog).delete()
    db.query(DeadLetterEvent).delete()
    db.commit()
    return {"success": True}


@app.get("/api/signatures", response_model=List[SignatureTemplateSchema])
async def list_signature_templates(db: Session = Depends(get_db)):
    return SignatureService.list_templates(session=db)


@app.put("/api/signatures/{source}", response_model=SignatureTemplateSchema)
async def update_signature_template(source: str, payload: SignatureTemplateUpdate, db: Session = Depends(get_db)):
    try:
        return SignatureService.update_template(source, payload, session=db)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/signatures/{source}/test", response_model=SignatureTestResponse)
async def test_signature(source: str, body: SignatureTestRequest, db: Session = Depends(get_db)):
    """根据已启用模板生成示例签名头，便于对接方测试。"""
    try:
        raw = json.dumps(body.payload or {"hello": "world"}, ensure_ascii=False).encode("utf-8")
        header, value = SignatureService.generate_header_value(source, raw, timestamp=body.timestamp, session=db)
        example_body = json.dumps(body.payload or {"hello": "world"}, ensure_ascii=False)
        curl = (
            f"curl -X POST https://your-endpoint \\\n  -H '{header}: {value}' \\\n  -H 'Content-Type: application/json' \\\n  -d '{example_body}'"
        )
        return SignatureTestResponse(header=header, value=value, example_curl=curl)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/dlq", response_model=PaginatedDeadLetters)
async def list_dead_letters(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=200, description="每页数量"),
    source: Optional[str] = Query(None, description="按事件来源筛选"),
    event_type: Optional[str] = Query(None, description="按事件类型筛选"),
    search: Optional[str] = Query(None, description="关键字匹配 reason/last_error/source/event_type/payload"),
    min_retry: int = Query(0, ge=0, description="最小重试次数"),
    db: Session = Depends(get_db),
):
    query = (
        db.query(DeadLetterEvent)
        .outerjoin(Event, DeadLetterEvent.event_id == Event.id)
    )

    if source:
        query = query.filter(Event.source == source)
    if event_type:
        query = query.filter(Event.event_type == event_type)
    if min_retry:
        query = query.filter(DeadLetterEvent.retry_count >= min_retry)
    if search and search.strip():
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                DeadLetterEvent.reason.ilike(term),
                DeadLetterEvent.last_error.ilike(term),
                Event.source.ilike(term),
                Event.event_type.ilike(term),
                Event.payload.ilike(term),
            )
        )

    total = query.count()
    items = (
        query.order_by(desc(DeadLetterEvent.created_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    event_ids = [item.event_id for item in items if item.event_id]
    event_map: Dict[int, Event] = {}
    if event_ids:
        events = (
            db.query(Event)
            .filter(Event.id.in_(event_ids))
            .all()
        )
        event_map = {evt.id: evt for evt in events}

    results: List[DeadLetterSchema] = []
    for item in items:
        event = event_map.get(item.event_id)
        results.append(
            DeadLetterSchema(
                id=item.id,
                event_id=item.event_id,
                source=event.source if event else "unknown",
                event_type=event.event_type if event else None,
                target_url=item.target_url,
                reason=item.reason,
                last_error=item.last_error,
                retry_count=item.retry_count,
                created_at=item.created_at,
                updated_at=item.updated_at,
                payload_preview=(event.payload[:200] if event and event.payload else None),
            )
        )

    return PaginatedDeadLetters(total=total, page=page, page_size=page_size, items=results)


@app.post("/api/dlq/{dlq_id}/replay", response_model=ReplayResponse)
async def replay_dead_letter(dlq_id: int, target_url: Optional[str] = Query(None), db: Session = Depends(get_db)):
    dlq_item = db.query(DeadLetterEvent).filter(DeadLetterEvent.id == dlq_id).first()
    if not dlq_item:
        raise HTTPException(status_code=404, detail="Dead letter not found")

    event = db.query(Event).filter(Event.id == dlq_item.event_id).first()
    if not event:
        db.delete(dlq_item)
        db.commit()
        raise HTTPException(status_code=404, detail="Original event not found")

    forwarder = EventForwarder()
    url = target_url or dlq_item.target_url or settings.FORWARD_URL
    if not url:
        raise HTTPException(status_code=400, detail="No target URL provided")

    guard = evaluate_replay_guard(db, dlq_item.event_id, url)
    if guard:
        if guard.get("action") == "skip_success":
            db.delete(dlq_item)
            db.commit()
            return ReplayResponse(
                success=True,
                message=guard["message"],
                event_id=dlq_item.event_id,
                last_success_at=guard.get("last_success_at"),
                notes=guard.get("note"),
            )
        if guard.get("action") == "cooldown":
            return ReplayResponse(
                success=False,
                message=guard["message"],
                event_id=dlq_item.event_id,
                retry_after=guard.get("retry_after"),
                last_attempt_at=guard.get("last_attempt_at"),
            )

    success = await forwarder.replay_event(dlq_item.event_id, url)
    if success:
        db.delete(dlq_item)
        db.commit()
    else:
        db.commit()

    response = ReplayResponse(
        success=success,
        message="Replay succeeded" if success else "Replay failed",
        event_id=dlq_item.event_id,
    )
    if success:
        response.last_success_at = datetime.utcnow()
    else:
        response.last_attempt_at = datetime.utcnow()
    return response


@app.post("/api/dlq/replay/batch", response_model=BulkReplayResult)
async def replay_dead_letters_batch(payload: BulkReplayRequest, db: Session = Depends(get_db)):
    """批量重放死信事件"""

    forwarder = EventForwarder()
    success_ids: List[int] = []
    failed: Dict[int, str] = {}
    notes: Dict[int, str] = {}

    seen = set()
    unique_ids: List[int] = []
    for dlq_id in payload.ids:
        if dlq_id in seen:
            failed[dlq_id] = "Duplicate id ignored"
            continue
        seen.add(dlq_id)
        unique_ids.append(dlq_id)

    for dlq_id in unique_ids:
        dlq_item = db.query(DeadLetterEvent).filter(DeadLetterEvent.id == dlq_id).first()
        if not dlq_item:
            failed[dlq_id] = "Dead letter not found"
            continue

        event = db.query(Event).filter(Event.id == dlq_item.event_id).first()
        if not event:
            failed[dlq_id] = "Original event not found"
            db.delete(dlq_item)
            continue

        target = payload.target_url or dlq_item.target_url or settings.FORWARD_URL
        if not target:
            failed[dlq_id] = "No target URL provided"
            continue

        guard = evaluate_replay_guard(db, dlq_item.event_id, target)
        if guard:
            if guard.get("action") == "skip_success":
                success_ids.append(dlq_id)
                notes[dlq_id] = guard["message"]
                db.delete(dlq_item)
                continue
            if guard.get("action") == "cooldown":
                failed[dlq_id] = guard["message"]
                continue

        success = await forwarder.replay_event(dlq_item.event_id, target)
        if success:
            success_ids.append(dlq_id)
            db.delete(dlq_item)
        else:
            failed[dlq_id] = "Replay failed"

    db.commit()
    return BulkReplayResult(success_ids=success_ids, failed=failed, notes=notes)


@app.delete("/api/dlq/{dlq_id}")
async def delete_dead_letter(dlq_id: int, db: Session = Depends(get_db)):
    dlq_item = db.query(DeadLetterEvent).filter(DeadLetterEvent.id == dlq_id).first()
    if not dlq_item:
        raise HTTPException(status_code=404, detail="Dead letter not found")
    db.delete(dlq_item)
    db.commit()
    return {"success": True}


@app.post("/api/dlq/clear")
async def clear_dead_letters(db: Session = Depends(get_db)):
    """清空死信队列"""

    deleted = db.query(DeadLetterEvent).delete()
    db.commit()
    return {"success": True, "cleared": deleted}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

