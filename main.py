from pathlib import Path
from loguru import logger
from apscheduler.schedulers.blocking import BlockingScheduler

Path("data/logs").mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(
    "data/logs/trading_{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="30 days",
    encoding="utf-8",
    diagnose=False,
    backtrace=True,
)

from scanner import run_daily_scan
from worker import check_orders

def main():
    scheduler = BlockingScheduler(timezone="Europe/Berlin")
    scheduler.add_job(
        run_daily_scan,
        trigger="cron",
        day_of_week="mon-fri",
        hour=22,
        minute=30,
        id="daily_scanner",
        name="Daily market scanner",
        max_instances=1,
        coalesce=True
    )

    scheduler.add_job(
        check_orders,
        trigger="interval",
        minutes=3,
        id="order_monitor",
        max_instances=1,
        coalesce=True
    )

    scheduler.start()

if __name__ == "__main__":
    main()