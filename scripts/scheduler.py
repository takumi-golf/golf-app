import schedule
import time
import logging
from pathlib import Path
import sys

# プロジェクトのルートディレクトリを取得
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from scripts.scraper import main as run_scraper
from scripts.backup_database import main as run_backup

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(project_root / 'logs' / 'scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def schedule_tasks():
    """タスクのスケジューリング"""
    # スクレイピング: 毎週月曜日の午前3時に実行
    schedule.every().monday.at("03:00").do(run_scraper)
    
    # バックアップ: 毎日午前2時に実行
    schedule.every().day.at("02:00").do(run_backup)

    logger.info("Scheduler started")
    logger.info("Scraping scheduled: Every Monday at 03:00")
    logger.info("Backup scheduled: Every day at 02:00")

    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # 1分ごとにチェック
        except Exception as e:
            logger.error(f"Error in scheduler: {str(e)}")
            time.sleep(300)  # エラー時は5分待機

if __name__ == "__main__":
    schedule_tasks() 