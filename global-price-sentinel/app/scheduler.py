"""
定时任务调度器
"""
import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import yaml
from pathlib import Path

from app.settings import settings
from app.models import TargetConfig, init_db
from app.monitor import run_monitor_cycle
from app.webhooks import check_and_alert
from app.reporter import ReportGenerator


async def scheduled_monitor_task():
    """定时监控任务"""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始定时监控任务...")
    
    # 加载配置
    config_path = Path("configs/targets.yml")
    if not config_path.exists():
        print("[!] 未找到 targets.yml 配置文件")
        return
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    targets = [TargetConfig(**t) for t in config.get('targets', [])]
    enabled_targets = [t for t in targets if t.enabled]
    
    print(f"[*] 加载了 {len(enabled_targets)} 个启用的监控目标")
    
    if not enabled_targets:
        print("[!] 没有启用的监控目标")
        return
    
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
    
    print(f"[✓] HTML 报告: {html_report}")
    print(f"[✓] CSV 报告: {csv_report}")
    print(f"[✓] 定时监控任务完成\n")


async def start_scheduler():
    """启动定时调度器"""
    init_db()
    
    scheduler = AsyncIOScheduler()
    
    # 解析 Cron 表达式
    cron_parts = settings.CRON_SCHEDULE.split()
    if len(cron_parts) != 5:
        print(f"[!] 无效的 Cron 表达式: {settings.CRON_SCHEDULE}")
        return
    
    minute, hour, day, month, day_of_week = cron_parts
    
    # 添加定时任务
    trigger = CronTrigger(
        minute=minute,
        hour=hour,
        day=day,
        month=month,
        day_of_week=day_of_week
    )
    
    scheduler.add_job(
        scheduled_monitor_task,
        trigger=trigger,
        id='monitor_task',
        name='Price Monitor Task',
        replace_existing=True
    )
    
    print(f"[✓] 定时任务已启动")
    print(f"    调度规则: {settings.CRON_SCHEDULE}")
    print(f"    下次运行: {scheduler.get_job('monitor_task').next_run_time}")
    
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

