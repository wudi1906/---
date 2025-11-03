"""
定时任务调度器
"""
import asyncio
from datetime import datetime
from typing import Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import yaml
from pathlib import Path

from app.settings import settings
from app.models import TargetConfig, init_db, MonitorJobRun, SessionLocal
from app.monitor import run_monitor_cycle
from app.webhooks import check_and_alert
from app.reporter import ReportGenerator
from app.config_service import ConfigService

# 全局 scheduler 引用，便于 API 查询
scheduler_instance: Optional[AsyncIOScheduler] = None


def _record_job_run(status: str, message: str, started_at: datetime, finished_at: datetime):
    db = SessionLocal()
    try:
        run = MonitorJobRun(
            job_id="monitor_task",
            job_name="Price Monitor Task",
            status=status,
            message=message[:500] if message else None,
            started_at=started_at,
            finished_at=finished_at,
            duration_ms=int((finished_at - started_at).total_seconds() * 1000),
        )
        db.add(run)
        db.commit()
    except Exception as exc:
        db.rollback()
        print(f"[!] 记录任务日志失败: {exc}")
    finally:
        db.close()


async def scheduled_monitor_task():
    """定时监控任务"""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始定时监控任务...")
    started_at = datetime.utcnow()
    status = "success"
    message = "任务执行成功"

    # 加载配置
    config_path = Path("configs/targets.yml")
    if not config_path.exists():
        warning = "未找到 targets.yml 配置文件"
        print(f"[!] {warning}")
        _record_job_run("failed", warning, started_at, datetime.utcnow())
        return

    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    targets = [TargetConfig(**t) for t in config.get('targets', [])]
    enabled_targets = [t for t in targets if t.enabled]

    print(f"[*] 加载了 {len(enabled_targets)} 个启用的监控目标")

    if not enabled_targets:
        warning = "没有启用的监控目标"
        print(f"[!] {warning}")
        _record_job_run("failed", warning, started_at, datetime.utcnow())
        return

    try:
        # 执行监控
        records = await run_monitor_cycle(enabled_targets)

        # 检查价格变动并发送告警
        print("\n[*] 检查价格变动...")
        for target in enabled_targets:
            check_and_alert(target.id, target.threshold_pct)

        # 生成报告
        print("\n[*] 生成报告...")
        html_report = ReportGenerator.generate_html_report(days=settings.HISTORY_DAYS)
        csv_report = ReportGenerator.generate_csv_report(days=settings.HISTORY_DAYS)

        message = (
            f"完成 {len(records)} 条监控记录，报告: {html_report.name if hasattr(html_report, 'name') else html_report}"
        )
        print(f"[✓] HTML 报告: {html_report}")
        print(f"[✓] CSV 报告: {csv_report}")
        print(f"[✓] 定时监控任务完成\n")
        _record_job_run(status, message, started_at, datetime.utcnow())
    except Exception as exc:
        status = "failed"
        message = str(exc)
        _record_job_run(status, message, started_at, datetime.utcnow())
        raise


async def start_scheduler():
    """启动定时调度器"""
    init_db()
    config = ConfigService.get_config()
    global scheduler_instance

    scheduler = AsyncIOScheduler()
    scheduler_instance = scheduler

    if config.scheduler_mode == "interval":
        scheduler.add_job(
            scheduled_monitor_task,
            "interval",
            minutes=config.interval_minutes,
            id="monitor_task",
            name="Price Monitor Task",
            replace_existing=True,
        )
        print(f"[✓] 定时任务已启动 (Interval)")
        print(f"    间隔: {config.interval_minutes} 分钟")
    else:
        cron_parts = config.cron_expression.split()
        if len(cron_parts) != 5:
            raise ValueError(f"无效的 Cron 表达式: {config.cron_expression}")

        minute, hour, day, month, day_of_week = cron_parts
        trigger = CronTrigger(
            minute=minute,
            hour=hour,
            day=day,
            month=month,
            day_of_week=day_of_week,
        )

        scheduler.add_job(
            scheduled_monitor_task,
            trigger=trigger,
            id="monitor_task",
            name="Price Monitor Task",
            replace_existing=True,
        )
        print(f"[✓] 定时任务已启动 (Cron)")
        print(f"    调度规则: {config.cron_expression}")

    job = scheduler.get_job("monitor_task")
    if job:
        print(f"    下次运行: {job.next_run_time}")

    scheduler.start()

    try:
        # 保持运行
        while True:
            await asyncio.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        print("\n[*] 停止调度器...")
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(start_scheduler())

