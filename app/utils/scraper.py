import requests
from bs4 import BeautifulSoup
import json
import time
import os
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
from app.config.scraper import ScraperConfig

class GolfClubScraper:
    """ゴルフクラブのスクレイピングクラス"""
    
    def __init__(self):
        self.config = ScraperConfig()
        self.session = requests.Session()
        self.setup_logging()
        
    def setup_logging(self):
        """ロギングの設定"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def get_page(self, url: str, params: Optional[Dict[str, Any]] = None) -> Optional[BeautifulSoup]:
        """ページを取得"""
        for attempt in range(self.config.MAX_RETRIES):
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                return BeautifulSoup(response.text, 'html.parser')
            except requests.RequestException as e:
                self.logger.error(f"Error fetching {url}: {e}")
                if attempt < self.config.MAX_RETRIES - 1:
                    time.sleep(self.config.RETRY_DELAY)
                else:
                    return None
                    
    def scrape_category(self, category: str) -> List[Dict[str, Any]]:
        """カテゴリごとのスクレイピング"""
        category_id = self.config.CATEGORY_IDS.get(category)
        if not category_id:
            self.logger.error(f"Invalid category: {category}")
            return []
            
        url = f"{self.config.BASE_URL}/spec-search"
        params = {"cat_id": category_id}
        
        clubs = []
        page = 1
        while True:
            params["page"] = page
            soup = self.get_page(url, params)
            if not soup:
                break
                
            # クラブ情報の取得
            club_elements = soup.select(".club-item")
            if not club_elements:
                break
                
            for element in club_elements:
                club = self.extract_club_info(element, category)
                if club:
                    clubs.append(club)
                    
            page += 1
            time.sleep(self.config.SCRAPING_INTERVAL)
            
        return clubs
        
    def extract_club_info(self, element: BeautifulSoup, category: str) -> Optional[Dict[str, Any]]:
        """クラブ情報の抽出"""
        try:
            # 基本情報
            name = element.select_one(".club-name").text.strip()
            manufacturer = element.select_one(".manufacturer").text.strip()
            
            # スペック情報
            specs = {}
            spec_elements = element.select(".spec-item")
            for spec in spec_elements:
                key = spec.select_one(".spec-label").text.strip()
                value = spec.select_one(".spec-value").text.strip()
                specs[key] = value
                
            # 特徴情報
            features = {}
            feature_elements = element.select(".feature-item")
            for feature in feature_elements:
                key = feature.select_one(".feature-label").text.strip()
                value = feature.select_one(".feature-value").text.strip()
                features[key] = value
                
            return {
                "name": name,
                "manufacturer": manufacturer,
                "category": category,
                "specs": specs,
                "features": features,
                "scraped_at": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error extracting club info: {e}")
            return None
            
    def save_data(self, data: List[Dict[str, Any]], category: str):
        """データの保存"""
        filename = self.config.DATA_FILES.get(category)
        if not filename:
            return
            
        # ディレクトリの作成
        os.makedirs(self.config.RAW_DATA_DIR, exist_ok=True)
        os.makedirs(self.config.PROCESSED_DATA_DIR, exist_ok=True)
        
        # 生データの保存
        raw_path = os.path.join(self.config.RAW_DATA_DIR, filename)
        with open(raw_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        # 処理済みデータの保存
        processed_data = self.process_data(data)
        processed_path = os.path.join(self.config.PROCESSED_DATA_DIR, filename)
        with open(processed_path, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, ensure_ascii=False, indent=2)
            
    def process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """データの処理"""
        processed = []
        for item in data:
            processed_item = {
                "name": item["name"],
                "manufacturer": item["manufacturer"],
                "category": item["category"],
                "specs": self.normalize_specs(item["specs"]),
                "features": self.normalize_features(item["features"]),
                "scraped_at": item["scraped_at"]
            }
            processed.append(processed_item)
        return processed
        
    def normalize_specs(self, specs: Dict[str, str]) -> Dict[str, Any]:
        """スペック情報の正規化"""
        normalized = {}
        for key, value in specs.items():
            # 数値の抽出
            if "°" in value:
                normalized[key] = float(value.replace("°", ""))
            elif "mm" in value:
                normalized[key] = float(value.replace("mm", ""))
            elif "g" in value:
                normalized[key] = float(value.replace("g", ""))
            else:
                normalized[key] = value
        return normalized
        
    def normalize_features(self, features: Dict[str, str]) -> Dict[str, float]:
        """特徴情報の正規化"""
        normalized = {}
        for key, value in features.items():
            # 5段階評価の数値化
            if "★" in value:
                normalized[key] = value.count("★")
            else:
                normalized[key] = 0
        return normalized
        
    def run(self):
        """スクレイピングの実行"""
        self.logger.info("Starting golf club scraping...")
        
        for category in self.config.CATEGORY_IDS.keys():
            self.logger.info(f"Scraping {category}...")
            clubs = self.scrape_category(category)
            self.save_data(clubs, category)
            self.logger.info(f"Scraped {len(clubs)} {category}")
            
        self.logger.info("Scraping completed") 