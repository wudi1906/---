# 国际化总体方案（Step 1 设计）

> 目标：为 Portal 及 6 个子项目提供统一的中/英文实时切换体验，保证页面、脚本提示、API 文案、演示流程均可根据语言偏好即时更新。

---

## 1. 用户入口：右上角语言切换组件

- **位置**：Portal 与所有子项目页面的右上角（与主题按钮并列），在 1280px 宽度下固定于顶部内边距 32px；在移动端折叠为悬浮按钮。
- **样式**：
  - 背景：半透明玻璃效果（rgba(15, 23, 42, 0.6) / rgba(255,255,255,0.2)），圆角 999px。
  - 显示：当前语言（`EN`/`中`）+ 地球图标；点击展开下拉（EN、中文），选中态高亮。
  - 无障碍：`aria-label="Switch language"`，键盘 `Enter`/`Space` 可切换。
- **脚本职责**：
  - 读取/写入全局语言状态。
  - 广播 `window.dispatchEvent(new CustomEvent('portfolio:lang-change', { detail: lang }))`，让各模块响应。

---

## 2. 语言状态存储策略

| 场景 | 优先级 | 说明 |
| --- | --- | --- |
| URL `?lang=` | 1 | 显式传参（分享链接）。从链接读取后写入 `localStorage` 并移除参数（history.replaceState）。 |
| `localStorage['portfolio-lang']` | 2 | Portal 与子项目共用 key。初始没有时走浏览器语言检测。 |
| 浏览器语言 | 3 | `navigator.language`，若前缀为 `zh` 则使用 `zh`, 否则 `en`。 |
| 服务器回退 | 4 | FastAPI/Next SSR 入口在未检测到客户端值时使用 `en`。 |

- **API 请求**：前端在 `fetch`/`axios` 时追加 `Accept-Language` 头；FastAPI 端读取并在响应内返回当前语言（若必要）。
- **持久化同步**：语言切换时写入 `localStorage` + 设置 Cookie `portfolio_lang`（供 FastAPI 模板初次渲染使用，7 天过期）。

---

## 3. 翻译资源结构

```
/i18n
  ├── portal.en.json
  ├── portal.zh.json
  ├── shared.en.json        # 通用按钮/提示
  ├── shared.zh.json
  ├── p1-price-sentinel.en.json
  ├── p1-price-sentinel.zh.json
  ...（P2~P6 同理）
```

- JSON 结构：扁平 key，允许嵌套对象，如 `"hero.title"`, `"cta.import"`。
- Portal 在加载时拉取 `portal.{lang}.json` + `shared.{lang}.json`；子项目加载对应 `pX-*.json`。
- FastAPI 项目使用 `Path(__file__).parent / "i18n" / f"p4-doc-knowledge.{lang}.json"` 等本地文件。
- React/Next/Storybook 项目将 JSON 放入 `public/i18n/`，使用 fetch 或 import。

### 示例（节选）
```json
{
  "hero.title": "Full-Stack Developer Portfolio",
  "hero.title_zh": "全栈开发作品集",          // 开发阶段存在同文件时临时保留
  "hero.subtitle": "6 Production-Ready Projects…",
  "cta.explore": "Explore Projects",
  "cta.explore.zh": "浏览项目"
}
```
> 实施时将 `.zh` 字段拆分为独立文件；此处仅为说明命名可读性。

---

## 4. Portal 实施要点（Step 2 准备）
- 在 `PORTAL_REDESIGN.html` 注入语言脚本：
  - 加载 `shared` + `portal` JSON。
  - 遍历包含 `data-i18n="hero.title"` 的元素，更新 `textContent`/`innerHTML`。
  - 对按钮/alt/title 属性使用 `data-i18n-attr="aria-label"` 方式更新。
- 切换机制：监听事件/按钮点击 → 更新 `currentLang` → 重绘。
- `import/reset` 成功/失败提示也走翻译表。

---

## 5. FastAPI 模板项目实施要点（Step 3 准备）
- 新增 `i18n.py` 辅助模块：
  ```python
  from functools import lru_cache
  from pathlib import Path
  import json

  BASE = Path(__file__).resolve().parent / "i18n"

  @lru_cache(maxsize=8)
  def load_translations(namespace: str, lang: str) -> dict:
      path = BASE / f"{namespace}.{lang}.json"
      fallback = BASE / f"{namespace}.en.json"
      return json.loads(path.read_text(encoding='utf-8')) if path.exists() else json.loads(fallback.read_text(encoding='utf-8'))
  ```
- 中间件 `lang_middleware`：读取查询、Cookie、`Accept-Language` → 注入 `request.state.lang`。
- Jinja2 模板新增过滤器 `{{ _('hero.title') }}`，由自定义函数从翻译字典取值。
- 前端 JS 同 Portal 脚本，监听 `portfolio:lang-change`。

---

## 6. React / Next / Storybook 项目实施要点（Step 4 准备）
- 引入轻量级国际化：
  - `saas-northstar-dashboard`（Next）：使用 `next-intl` 或自定义 Context（`LangProvider` + `useTranslation`）。
  - `a11y-component-atlas`（Vite/React）：使用 `i18next` 或 `valtio` + 自定义 hook。
- 共享语言状态：
  - 在 Portal 切换时写入 `localStorage`。
  - 每个 React 项目在 `useEffect` 中读取 `localStorage`，并监听 `storage` 事件或自定义 `portfolio:lang-change`。
- Storybook：添加全局装饰器 `<LanguageProvider>`，控制文案展示。

---

## 7. API 与提示多语言
- REST 接口返回的字符串（如上传成功/失败）读取翻译文件，默认英文。
- `fetch`/`axios` 请求 headers 添加 `Accept-Language: currentLang`，后端 `JSONResponse(headers={'Content-Language': lang})`。
- Console/logging 保留英文，面向用户界面/弹窗/Toast 切换语言。

---

## 8. 测试矩阵（Step 5 准备）
- 浏览器：Chrome / Edge / Safari；语言切换后刷新 → 语言保持。
- 深链接：`http://localhost:8101/?lang=zh` → 中文；切换为 English → 历史记录移除 `?lang=`。
- 跨页面：Portal 切换 → 打开 P2(8202) → 自动中文；返回 Portal 仍保持。
- API：上传/导出/Import/Reset 返回中文提示。

---

**Step 1 完成度：100%**（已确定入口组件、状态存储、翻译结构、API 约定及各项目实施策略，为后续落地提供参照）。
