import schedule
import time
from datetime import datetime
import logging
from app.utils.scraper import GolfClubScraper
from app.config.scraper import ScraperConfig

class ScraperScheduler:
    """スクレイピングのスケジューラー"""
    
    def __init__(self):
        self.config = ScraperConfig()
        self.scraper = GolfClubScraper()
        self.setup_logging()
        
    def setup_logging(self):
        """ロギングの設定"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/scheduler.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def run_scraper(self):
        """スクレイピングの実行"""
        self.logger.info("Starting scheduled scraping...")
        try:
            self.scraper.run()
            self.logger.info("Scheduled scraping completed successfully")
        except Exception as e:
            self.logger.error(f"Error in scheduled scraping: {e}")
            
    def start(self):
        """スケジューラーの開始"""
        if self.config.SCHEDULE["daily"]:
            schedule.every().day.at(self.config.SCHEDULE["time"]).do(self.run_scraper)
            
        self.logger.info("Scheduler started")
        while True:
            schedule.run_pending()
            time.sleep(60)
            
if __name__ == "__main__":
    scheduler = ScraperScheduler()
    scheduler.start() 