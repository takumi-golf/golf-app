import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from datetime import datetime
import logging
import os
from typing import Dict, List, Optional
import re

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

class GolfClubScraper:
    def __init__(self):
        self.base_url = "https://golfdigest.impress.co.jp"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def get_club_list(self, page: int = 1) -> List[Dict]:
        """クラブ一覧ページからクラブ情報を取得"""
        url = f"{self.base_url}/club/ranking/"
        if page > 1:
            url += f"page{page}/"
            
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            clubs = []
            for item in soup.select('.club-ranking-item'):
                try:
                    club = {
                        'name': item.select_one('.club-name').text.strip(),
                        'brand': item.select_one('.club-brand').text.strip(),
                        'url': self.base_url + item.select_one('a')['href'],
                        'category': item.select_one('.club-category').text.strip(),
                        'price': self._extract_price(item.select_one('.club-price').text.strip()),
                        'release_date': self._extract_date(item.select_one('.club-date').text.strip()),
                        'rating': float(item.select_one('.club-rating').text.strip()),
                        'review_count': int(item.select_one('.club-review-count').text.strip().replace('件', '')),
                        'image_url': item.select_one('img')['src']
                    }
                    clubs.append(club)
                except Exception as e:
                    logging.error(f"クラブ情報の解析中にエラー: {e}")
                    continue
                    
            return clubs
        except Exception as e:
            logging.error(f"クラブ一覧の取得中にエラー: {e}")
            return []
            
    def get_club_detail(self, url: str) -> Dict:
        """クラブの詳細情報を取得"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            detail = {
                'specs': self._extract_specs(soup),
                'features': self._extract_features(soup),
                'reviews': self._extract_reviews(soup),
                'shaft_options': self._extract_shaft_options(soup),
                'grip_options': self._extract_grip_options(soup),
                'comparison': self._extract_comparison(soup),
                'awards': self._extract_awards(soup)
            }
            
            return detail
        except Exception as e:
            logging.error(f"クラブ詳細の取得中にエラー: {e}")
            return {}
            
    def _extract_specs(self, soup: BeautifulSoup) -> Dict:
        """仕様情報を抽出"""
        specs = {}
        try:
            specs_table = soup.select_one('.club-specs-table')
            if specs_table:
                for row in specs_table.select('tr'):
                    key = row.select_one('th').text.strip()
                    value = row.select_one('td').text.strip()
                    specs[key] = value
        except Exception as e:
            logging.error(f"仕様情報の抽出中にエラー: {e}")
        return specs
        
    def _extract_features(self, soup: BeautifulSoup) -> List[str]:
        """特徴情報を抽出"""
        features = []
        try:
            features_section = soup.select_one('.club-features')
            if features_section:
                features = [f.text.strip() for f in features_section.select('li')]
        except Exception as e:
            logging.error(f"特徴情報の抽出中にエラー: {e}")
        return features
        
    def _extract_reviews(self, soup: BeautifulSoup) -> List[Dict]:
        """レビュー情報を抽出"""
        reviews = []
        try:
            reviews_section = soup.select('.club-review')
            for review in reviews_section:
                try:
                    review_data = {
                        'rating': float(review.select_one('.review-rating').text.strip()),
                        'comment': review.select_one('.review-comment').text.strip(),
                        'date': self._extract_date(review.select_one('.review-date').text.strip()),
                        'user': review.select_one('.review-user').text.strip(),
                        'handicap': float(review.select_one('.review-handicap').text.strip().replace('HCP', '')),
                        'swing_speed': float(review.select_one('.review-swing-speed').text.strip().replace('m/s', '')),
                        'ball_speed': float(review.select_one('.review-ball-speed').text.strip().replace('m/s', '')),
                        'carry_distance': float(review.select_one('.review-carry').text.strip().replace('ヤード', '')),
                        'total_distance': float(review.select_one('.review-total').text.strip().replace('ヤード', '')),
                        'launch_angle': float(review.select_one('.review-launch').text.strip().replace('°', '')),
                        'spin_rate': float(review.select_one('.review-spin').text.strip().replace('rpm', '')),
                        'shot_shape': review.select_one('.review-shot-shape').text.strip(),
                        'feel': review.select_one('.review-feel').text.strip(),
                        'forgiveness': review.select_one('.review-forgiveness').text.strip(),
                        'workability': review.select_one('.review-workability').text.strip()
                    }
                    reviews.append(review_data)
                except Exception as e:
                    logging.error(f"レビュー情報の解析中にエラー: {e}")
                    continue
        except Exception as e:
            logging.error(f"レビュー情報の抽出中にエラー: {e}")
        return reviews
        
    def _extract_shaft_options(self, soup: BeautifulSoup) -> List[Dict]:
        """シャフトオプション情報を抽出"""
        shafts = []
        try:
            shafts_section = soup.select('.shaft-option')
            for shaft in shafts_section:
                try:
                    shaft_data = {
                        'name': shaft.select_one('.shaft-name').text.strip(),
                        'brand': shaft.select_one('.shaft-brand').text.strip(),
                        'flex': shaft.select_one('.shaft-flex').text.strip(),
                        'weight': float(shaft.select_one('.shaft-weight').text.strip().replace('g', '')),
                        'torque': float(shaft.select_one('.shaft-torque').text.strip().replace('°', '')),
                        'kick_point': shaft.select_one('.shaft-kick-point').text.strip(),
                        'price': self._extract_price(shaft.select_one('.shaft-price').text.strip())
                    }
                    shafts.append(shaft_data)
                except Exception as e:
                    logging.error(f"シャフト情報の解析中にエラー: {e}")
                    continue
        except Exception as e:
            logging.error(f"シャフト情報の抽出中にエラー: {e}")
        return shafts
        
    def _extract_grip_options(self, soup: BeautifulSoup) -> List[Dict]:
        """グリップオプション情報を抽出"""
        grips = []
        try:
            grips_section = soup.select('.grip-option')
            for grip in grips_section:
                try:
                    grip_data = {
                        'name': grip.select_one('.grip-name').text.strip(),
                        'brand': grip.select_one('.grip-brand').text.strip(),
                        'size': grip.select_one('.grip-size').text.strip(),
                        'material': grip.select_one('.grip-material').text.strip(),
                        'weight': float(grip.select_one('.grip-weight').text.strip().replace('g', '')),
                        'price': self._extract_price(grip.select_one('.grip-price').text.strip())
                    }
                    grips.append(grip_data)
                except Exception as e:
                    logging.error(f"グリップ情報の解析中にエラー: {e}")
                    continue
        except Exception as e:
            logging.error(f"グリップ情報の抽出中にエラー: {e}")
        return grips
        
    def _extract_comparison(self, soup: BeautifulSoup) -> Dict:
        """比較情報を抽出"""
        comparison = {}
        try:
            comparison_section = soup.select_one('.club-comparison')
            if comparison_section:
                for item in comparison_section.select('.comparison-item'):
                    key = item.select_one('.comparison-key').text.strip()
                    value = item.select_one('.comparison-value').text.strip()
                    comparison[key] = value
        except Exception as e:
            logging.error(f"比較情報の抽出中にエラー: {e}")
        return comparison
        
    def _extract_awards(self, soup: BeautifulSoup) -> List[Dict]:
        """受賞情報を抽出"""
        awards = []
        try:
            awards_section = soup.select('.club-award')
            for award in awards_section:
                try:
                    award_data = {
                        'name': award.select_one('.award-name').text.strip(),
                        'year': int(award.select_one('.award-year').text.strip()),
                        'category': award.select_one('.award-category').text.strip(),
                        'rank': int(award.select_one('.award-rank').text.strip().replace('位', ''))
                    }
                    awards.append(award_data)
                except Exception as e:
                    logging.error(f"受賞情報の解析中にエラー: {e}")
                    continue
        except Exception as e:
            logging.error(f"受賞情報の抽出中にエラー: {e}")
        return awards
        
    def _extract_price(self, text: str) -> Optional[float]:
        """価格情報を抽出"""
        try:
            price = re.search(r'[\d,]+', text)
            if price:
                return float(price.group().replace(',', ''))
        except Exception as e:
            logging.error(f"価格情報の抽出中にエラー: {e}")
        return None
        
    def _extract_date(self, text: str) -> Optional[str]:
        """日付情報を抽出"""
        try:
            date = re.search(r'\d{4}/\d{1,2}/\d{1,2}', text)
            if date:
                return date.group()
        except Exception as e:
            logging.error(f"日付情報の抽出中にエラー: {e}")
        return None
        
    def scrape_all(self, max_pages: int = 5) -> List[Dict]:
        """全てのクラブ情報を取得"""
        all_clubs = []
        
        for page in range(1, max_pages + 1):
            logging.info(f"ページ {page} のクラブ情報を取得中...")
            clubs = self.get_club_list(page)
            
            for club in clubs:
                try:
                    logging.info(f"クラブ詳細を取得中: {club['name']}")
                    detail = self.get_club_detail(club['url'])
                    club.update(detail)
                    all_clubs.append(club)
                    
                    # ランダムな待機時間を設定
                    time.sleep(random.uniform(1, 3))
                except Exception as e:
                    logging.error(f"クラブ詳細の取得中にエラー: {e}")
                    continue
                    
        return all_clubs
        
    def save_to_csv(self, clubs: List[Dict], filename: str = 'golf_clubs.csv'):
        """データをCSVファイルに保存"""
        try:
            df = pd.DataFrame(clubs)
            df.to_csv(filename, index=False, encoding='utf-8')
            logging.info(f"データを {filename} に保存しました")
        except Exception as e:
            logging.error(f"データの保存中にエラー: {e}")

if __name__ == "__main__":
    scraper = GolfClubScraper()
    clubs = scraper.scrape_all()
    scraper.save_to_csv(clubs) 