import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict
import logging
from datetime import datetime
import time
import random

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ClubScraper:
    def __init__(self):
        self.base_url = "https://www.golfdigest.co.jp/club/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_club_categories(self) -> List[Dict[str, str]]:
        """クラブのカテゴリー一覧を取得"""
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            categories = []
            category_elements = soup.select('.category-list a')
            
            for element in category_elements:
                categories.append({
                    'name': element.text.strip(),
                    'url': element['href']
                })
            
            return categories
        except Exception as e:
            logger.error(f"カテゴリー取得中にエラーが発生しました: {e}")
            return []

    def get_club_list(self, category_url: str) -> List[Dict[str, str]]:
        """カテゴリー内のクラブ一覧を取得"""
        try:
            response = self.session.get(category_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            clubs = []
            club_elements = soup.select('.club-list-item')
            
            for element in club_elements:
                clubs.append({
                    'name': element.select_one('.club-name').text.strip(),
                    'brand': element.select_one('.brand-name').text.strip(),
                    'url': element.select_one('a')['href'],
                    'price': element.select_one('.price').text.strip() if element.select_one('.price') else None,
                    'category': category_url.split('/')[-2]
                })
            
            return clubs
        except Exception as e:
            logger.error(f"クラブ一覧取得中にエラーが発生しました: {e}")
            return []

    def get_club_details(self, club_url: str) -> Dict:
        """クラブの詳細情報を取得"""
        try:
            response = self.session.get(club_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            details = {
                'name': soup.select_one('.club-name').text.strip(),
                'brand': soup.select_one('.brand-name').text.strip(),
                'price': soup.select_one('.price').text.strip() if soup.select_one('.price') else None,
                'specifications': {},
                'features': [],
                'reviews': []
            }
            
            # 仕様情報の取得
            spec_elements = soup.select('.specifications-table tr')
            for element in spec_elements:
                key = element.select_one('th').text.strip()
                value = element.select_one('td').text.strip()
                details['specifications'][key] = value
            
            # 特徴の取得
            feature_elements = soup.select('.features-list li')
            for element in feature_elements:
                details['features'].append(element.text.strip())
            
            # レビューの取得
            review_elements = soup.select('.review-item')
            for element in review_elements:
                details['reviews'].append({
                    'rating': element.select_one('.rating').text.strip(),
                    'comment': element.select_one('.comment').text.strip(),
                    'date': element.select_one('.date').text.strip()
                })
            
            return details
        except Exception as e:
            logger.error(f"クラブ詳細取得中にエラーが発生しました: {e}")
            return {}

    def scrape_all_clubs(self) -> List[Dict]:
        """すべてのクラブ情報を収集"""
        all_clubs = []
        
        # カテゴリー一覧を取得
        categories = self.get_club_categories()
        logger.info(f"カテゴリー数: {len(categories)}")
        
        for category in categories:
            logger.info(f"カテゴリー '{category['name']}' のクラブを収集中...")
            
            # クラブ一覧を取得
            clubs = self.get_club_list(category['url'])
            logger.info(f"クラブ数: {len(clubs)}")
            
            for club in clubs:
                # 詳細情報を取得
                details = self.get_club_details(club['url'])
                club.update(details)
                all_clubs.append(club)
                
                # サーバーに負荷をかけないようにランダムな待機時間を設定
                time.sleep(random.uniform(1, 3))
        
        return all_clubs

def main():
    scraper = ClubScraper()
    
    # クラブ情報を収集
    logger.info("クラブ情報の収集を開始します...")
    clubs = scraper.scrape_all_clubs()
    
    # データフレームに変換
    df = pd.DataFrame(clubs)
    
    # CSVファイルとして保存
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"club_data_{timestamp}.csv"
    df.to_csv(filename, index=False, encoding='utf-8')
    
    logger.info(f"クラブ情報を {filename} に保存しました。")
    logger.info(f"収集したクラブ数: {len(clubs)}")

if __name__ == "__main__":
    main() 