import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path
import time
import json
from db_connection import DatabaseConnection

def setup_logging():
    """ロギングの設定を行います。"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('database/scraper.log'),
            logging.StreamHandler()
        ]
    )

class GolfClubScraper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.base_urls = {
            'titleist': 'https://www.titleist.com',
            'callaway': 'https://www.callawaygolf.com',
            'taylormade': 'https://www.taylormadegolf.com',
            'ping': 'https://www.ping.com',
            'mizuno': 'https://www.mizunogolf.com',
            'srixon': 'https://www.srixon.com',
            'cobra': 'https://www.cobragolf.com',
            'honma': 'https://www.honmagolf.com'
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def fetch_manufacturer_data(self, manufacturer: str) -> List[Dict]:
        """メーカーのゴルフクラブデータを取得します。"""
        try:
            self.logger.info(f"{manufacturer}のデータ取得を開始します...")
            
            if manufacturer not in self.base_urls:
                raise ValueError(f"未対応のメーカーです: {manufacturer}")
                
            url = self.base_urls[manufacturer]
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # メーカーごとのスクレイピングロジックを実装
            clubs = []
            if manufacturer == 'titleist':
                clubs = self._scrape_titleist(soup)
            elif manufacturer == 'callaway':
                clubs = self._scrape_callaway(soup)
            elif manufacturer == 'taylormade':
                clubs = self._scrape_taylormade(soup)
            elif manufacturer == 'ping':
                clubs = self._scrape_ping(soup)
            elif manufacturer == 'mizuno':
                clubs = self._scrape_mizuno(soup)
            elif manufacturer == 'srixon':
                clubs = self._scrape_srixon(soup)
            elif manufacturer == 'cobra':
                clubs = self._scrape_cobra(soup)
            elif manufacturer == 'honma':
                clubs = self._scrape_honma(soup)
            # 他のメーカーのスクレイピングロジックを追加
                
            self.logger.info(f"{manufacturer}から{len(clubs)}件のデータを取得しました。")
            return clubs
            
        except Exception as e:
            self.logger.error(f"{manufacturer}のデータ取得中にエラーが発生しました: {str(e)}")
            return []
            
    def _scrape_titleist(self, soup: BeautifulSoup) -> List[Dict]:
        """Titleistのゴルフクラブデータをスクレイピングします。"""
        clubs = []
        try:
            # Titleistの製品ページURL
            product_url = "https://www.titleist.com/golf-clubs"
            response = requests.get(product_url, headers=self.headers)
            response.raise_for_status()
            product_soup = BeautifulSoup(response.text, 'html.parser')
            
            # 製品カテゴリーのリンクを取得
            category_links = product_soup.select('.product-category a')
            for category_link in category_links:
                category_url = category_link['href']
                if not category_url.startswith('http'):
                    category_url = f"https://www.titleist.com{category_url}"
                
                # カテゴリーページにアクセス
                category_response = requests.get(category_url, headers=self.headers)
                category_response.raise_for_status()
                category_soup = BeautifulSoup(category_response.text, 'html.parser')
                
                # 製品カードを取得
                product_cards = category_soup.select('.product-card')
                for card in product_cards:
                    try:
                        # 製品詳細ページのURLを取得
                        product_detail_url = card.select_one('a')['href']
                        if not product_detail_url.startswith('http'):
                            product_detail_url = f"https://www.titleist.com{product_detail_url}"
                        
                        # 製品詳細ページにアクセス
                        detail_response = requests.get(product_detail_url, headers=self.headers)
                        detail_response.raise_for_status()
                        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
                        
                        # 製品情報を抽出
                        club_data = {
                            'manufacturer': 'Titleist',
                            'country': 'USA',
                            'website': self.base_urls['titleist'],
                            'established_year': 1932,
                            'series': detail_soup.select_one('.product-series').text.strip() if detail_soup.select_one('.product-series') else '',
                            'model': detail_soup.select_one('.product-name').text.strip() if detail_soup.select_one('.product-name') else '',
                            'club_type': category_link.text.strip().lower(),
                            'loft_range': detail_soup.select_one('.loft-range').text.strip() if detail_soup.select_one('.loft-range') else '',
                            'length_range': detail_soup.select_one('.length-range').text.strip() if detail_soup.select_one('.length-range') else '',
                            'weight_range': detail_soup.select_one('.weight-range').text.strip() if detail_soup.select_one('.weight-range') else '',
                            'stock_options': {
                                'shafts': [s.text.strip() for s in detail_soup.select('.stock-shafts .shaft')],
                                'grips': [g.text.strip() for g in detail_soup.select('.stock-grips .grip')]
                            },
                            'msrp': float(detail_soup.select_one('.price').text.strip().replace('$', '').replace(',', '')) if detail_soup.select_one('.price') else 0.0,
                            'release_year': int(detail_soup.select_one('.release-year').text.strip()) if detail_soup.select_one('.release-year') else datetime.now().year
                        }
                        clubs.append(club_data)
                        
                        # サーバーへの負荷を考慮して待機
                        time.sleep(2)
                        
                    except Exception as e:
                        self.logger.error(f"製品詳細のスクレイピング中にエラーが発生しました: {str(e)}")
                        continue
                
                # カテゴリー間の待機
                time.sleep(3)
            
            self.logger.info(f"Titleistから{len(clubs)}件のデータを取得しました。")
            
        except Exception as e:
            self.logger.error(f"Titleistのスクレイピング中にエラーが発生しました: {str(e)}")
            
        return clubs
        
    def _scrape_callaway(self, soup: BeautifulSoup) -> List[Dict]:
        """Callawayのゴルフクラブデータをスクレイピングします。"""
        clubs = []
        try:
            # Callawayの製品ページURL
            product_url = "https://www.callawaygolf.com/golf-clubs"
            response = requests.get(product_url, headers=self.headers)
            response.raise_for_status()
            product_soup = BeautifulSoup(response.text, 'html.parser')
            
            # 製品カテゴリーのリンクを取得
            category_links = product_soup.select('.product-category a')
            for category_link in category_links:
                category_url = category_link['href']
                if not category_url.startswith('http'):
                    category_url = f"https://www.callawaygolf.com{category_url}"
                
                # カテゴリーページにアクセス
                category_response = requests.get(category_url, headers=self.headers)
                category_response.raise_for_status()
                category_soup = BeautifulSoup(category_response.text, 'html.parser')
                
                # 製品カードを取得
                product_cards = category_soup.select('.product-card')
                for card in product_cards:
                    try:
                        # 製品詳細ページのURLを取得
                        product_detail_url = card.select_one('a')['href']
                        if not product_detail_url.startswith('http'):
                            product_detail_url = f"https://www.callawaygolf.com{product_detail_url}"
                        
                        # 製品詳細ページにアクセス
                        detail_response = requests.get(product_detail_url, headers=self.headers)
                        detail_response.raise_for_status()
                        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
                        
                        # 製品情報を抽出
                        club_data = {
                            'manufacturer': 'Callaway',
                            'country': 'USA',
                            'website': self.base_urls['callaway'],
                            'established_year': 1982,
                            'series': detail_soup.select_one('.product-series').text.strip() if detail_soup.select_one('.product-series') else '',
                            'model': detail_soup.select_one('.product-name').text.strip() if detail_soup.select_one('.product-name') else '',
                            'club_type': category_link.text.strip().lower(),
                            'loft_range': detail_soup.select_one('.loft-range').text.strip() if detail_soup.select_one('.loft-range') else '',
                            'length_range': detail_soup.select_one('.length-range').text.strip() if detail_soup.select_one('.length-range') else '',
                            'weight_range': detail_soup.select_one('.weight-range').text.strip() if detail_soup.select_one('.weight-range') else '',
                            'stock_options': {
                                'shafts': [s.text.strip() for s in detail_soup.select('.stock-shafts .shaft')],
                                'grips': [g.text.strip() for g in detail_soup.select('.stock-grips .grip')]
                            },
                            'msrp': float(detail_soup.select_one('.price').text.strip().replace('$', '').replace(',', '')) if detail_soup.select_one('.price') else 0.0,
                            'release_year': int(detail_soup.select_one('.release-year').text.strip()) if detail_soup.select_one('.release-year') else datetime.now().year
                        }
                        clubs.append(club_data)
                        
                        # サーバーへの負荷を考慮して待機
                        time.sleep(2)
                        
                    except Exception as e:
                        self.logger.error(f"製品詳細のスクレイピング中にエラーが発生しました: {str(e)}")
                        continue
                
                # カテゴリー間の待機
                time.sleep(3)
            
            self.logger.info(f"Callawayから{len(clubs)}件のデータを取得しました。")
            
        except Exception as e:
            self.logger.error(f"Callawayのスクレイピング中にエラーが発生しました: {str(e)}")
            
        return clubs
        
    def _scrape_taylormade(self, soup: BeautifulSoup) -> List[Dict]:
        """TaylorMadeのゴルフクラブデータをスクレイピングします。"""
        clubs = []
        try:
            # ドライバーのデータを取得
            driver_url = f"{self.base_urls['taylormade']}/golf-clubs/drivers"
            response = requests.get(driver_url, headers=self.headers)
            response.raise_for_status()
            driver_soup = BeautifulSoup(response.text, 'html.parser')
            
            # ドライバーのモデルを取得
            driver_models = driver_soup.select('.product-card')
            for model in driver_models:
                club_data = {
                    'manufacturer': 'TaylorMade',
                    'country': 'USA',
                    'website': self.base_urls['taylormade'],
                    'established_year': 1979,
                    'series': model.select_one('.series-name').text.strip(),
                    'model': model.select_one('.model-name').text.strip(),
                    'club_type': 'driver',
                    'loft_range': model.select_one('.loft-range').text.strip(),
                    'length_range': model.select_one('.length-range').text.strip(),
                    'weight_range': model.select_one('.weight-range').text.strip(),
                    'stock_options': {
                        'shafts': [s.text.strip() for s in model.select('.stock-shafts .shaft')],
                        'grips': [g.text.strip() for g in model.select('.stock-grips .grip')]
                    },
                    'msrp': float(model.select_one('.price').text.strip().replace('¥', '').replace(',', '')),
                    'release_year': int(model.select_one('.release-year').text.strip())
                }
                clubs.append(club_data)
                
            # アイアンのデータを取得
            iron_url = f"{self.base_urls['taylormade']}/golf-clubs/irons"
            response = requests.get(iron_url, headers=self.headers)
            response.raise_for_status()
            iron_soup = BeautifulSoup(response.text, 'html.parser')
            
            # アイアンのモデルを取得
            iron_models = iron_soup.select('.product-card')
            for model in iron_models:
                club_data = {
                    'manufacturer': 'TaylorMade',
                    'country': 'USA',
                    'website': self.base_urls['taylormade'],
                    'established_year': 1979,
                    'series': model.select_one('.series-name').text.strip(),
                    'model': model.select_one('.model-name').text.strip(),
                    'club_type': 'iron',
                    'loft_range': model.select_one('.loft-range').text.strip(),
                    'length_range': model.select_one('.length-range').text.strip(),
                    'weight_range': model.select_one('.weight-range').text.strip(),
                    'stock_options': {
                        'shafts': [s.text.strip() for s in model.select('.stock-shafts .shaft')],
                        'grips': [g.text.strip() for g in model.select('.stock-grips .grip')]
                    },
                    'msrp': float(model.select_one('.price').text.strip().replace('¥', '').replace(',', '')),
                    'release_year': int(model.select_one('.release-year').text.strip())
                }
                clubs.append(club_data)
                
            # ウェッジのデータを取得
            wedge_url = f"{self.base_urls['taylormade']}/golf-clubs/wedges"
            response = requests.get(wedge_url, headers=self.headers)
            response.raise_for_status()
            wedge_soup = BeautifulSoup(response.text, 'html.parser')
            
            # ウェッジのモデルを取得
            wedge_models = wedge_soup.select('.product-card')
            for model in wedge_models:
                club_data = {
                    'manufacturer': 'TaylorMade',
                    'country': 'USA',
                    'website': self.base_urls['taylormade'],
                    'established_year': 1979,
                    'series': model.select_one('.series-name').text.strip(),
                    'model': model.select_one('.model-name').text.strip(),
                    'club_type': 'wedge',
                    'loft_range': model.select_one('.loft-range').text.strip(),
                    'length_range': model.select_one('.length-range').text.strip(),
                    'weight_range': model.select_one('.weight-range').text.strip(),
                    'stock_options': {
                        'shafts': [s.text.strip() for s in model.select('.stock-shafts .shaft')],
                        'grips': [g.text.strip() for g in model.select('.stock-grips .grip')]
                    },
                    'msrp': float(model.select_one('.price').text.strip().replace('¥', '').replace(',', '')),
                    'release_year': int(model.select_one('.release-year').text.strip())
                }
                clubs.append(club_data)
                
            self.logger.info(f"TaylorMadeから{len(clubs)}件のデータを取得しました。")
            
        except Exception as e:
            self.logger.error(f"TaylorMadeのスクレイピング中にエラーが発生しました: {str(e)}")
            
        return clubs
        
    def _scrape_ping(self, soup: BeautifulSoup) -> List[Dict]:
        """PINGのゴルフクラブデータをスクレイピングします。"""
        clubs = []
        try:
            # ドライバーのデータを取得
            driver_url = f"{self.base_urls['ping']}/golf-clubs/drivers"
            response = requests.get(driver_url, headers=self.headers)
            response.raise_for_status()
            driver_soup = BeautifulSoup(response.text, 'html.parser')
            
            # ドライバーのモデルを取得
            driver_models = driver_soup.select('.product-card')
            for model in driver_models:
                club_data = {
                    'manufacturer': 'PING',
                    'country': 'USA',
                    'website': self.base_urls['ping'],
                    'established_year': 1959,
                    'series': model.select_one('.series-name').text.strip(),
                    'model': model.select_one('.model-name').text.strip(),
                    'club_type': 'driver',
                    'loft_range': model.select_one('.loft-range').text.strip(),
                    'length_range': model.select_one('.length-range').text.strip(),
                    'weight_range': model.select_one('.weight-range').text.strip(),
                    'stock_options': {
                        'shafts': [s.text.strip() for s in model.select('.stock-shafts .shaft')],
                        'grips': [g.text.strip() for g in model.select('.stock-grips .grip')]
                    },
                    'msrp': float(model.select_one('.price').text.strip().replace('¥', '').replace(',', '')),
                    'release_year': int(model.select_one('.release-year').text.strip())
                }
                clubs.append(club_data)
                
            # アイアンのデータを取得
            iron_url = f"{self.base_urls['ping']}/golf-clubs/irons"
            response = requests.get(iron_url, headers=self.headers)
            response.raise_for_status()
            iron_soup = BeautifulSoup(response.text, 'html.parser')
            
            # アイアンのモデルを取得
            iron_models = iron_soup.select('.product-card')
            for model in iron_models:
                club_data = {
                    'manufacturer': 'PING',
                    'country': 'USA',
                    'website': self.base_urls['ping'],
                    'established_year': 1959,
                    'series': model.select_one('.series-name').text.strip(),
                    'model': model.select_one('.model-name').text.strip(),
                    'club_type': 'iron',
                    'loft_range': model.select_one('.loft-range').text.strip(),
                    'length_range': model.select_one('.length-range').text.strip(),
                    'weight_range': model.select_one('.weight-range').text.strip(),
                    'stock_options': {
                        'shafts': [s.text.strip() for s in model.select('.stock-shafts .shaft')],
                        'grips': [g.text.strip() for g in model.select('.stock-grips .grip')]
                    },
                    'msrp': float(model.select_one('.price').text.strip().replace('¥', '').replace(',', '')),
                    'release_year': int(model.select_one('.release-year').text.strip())
                }
                clubs.append(club_data)
                
            # ウェッジのデータを取得
            wedge_url = f"{self.base_urls['ping']}/golf-clubs/wedges"
            response = requests.get(wedge_url, headers=self.headers)
            response.raise_for_status()
            wedge_soup = BeautifulSoup(response.text, 'html.parser')
            
            # ウェッジのモデルを取得
            wedge_models = wedge_soup.select('.product-card')
            for model in wedge_models:
                club_data = {
                    'manufacturer': 'PING',
                    'country': 'USA',
                    'website': self.base_urls['ping'],
                    'established_year': 1959,
                    'series': model.select_one('.series-name').text.strip(),
                    'model': model.select_one('.model-name').text.strip(),
                    'club_type': 'wedge',
                    'loft_range': model.select_one('.loft-range').text.strip(),
                    'length_range': model.select_one('.length-range').text.strip(),
                    'weight_range': model.select_one('.weight-range').text.strip(),
                    'stock_options': {
                        'shafts': [s.text.strip() for s in model.select('.stock-shafts .shaft')],
                        'grips': [g.text.strip() for g in model.select('.stock-grips .grip')]
                    },
                    'msrp': float(model.select_one('.price').text.strip().replace('¥', '').replace(',', '')),
                    'release_year': int(model.select_one('.release-year').text.strip())
                }
                clubs.append(club_data)
                
            self.logger.info(f"PINGから{len(clubs)}件のデータを取得しました。")
            
        except Exception as e:
            self.logger.error(f"PINGのスクレイピング中にエラーが発生しました: {str(e)}")
            
        return clubs
        
    def _scrape_mizuno(self, soup: BeautifulSoup) -> List[Dict]:
        """Mizunoのゴルフクラブデータをスクレイピングします。"""
        clubs = []
        try:
            # ドライバーのデータを取得
            driver_url = f"{self.base_urls['mizuno']}/golf-clubs/drivers"
            response = requests.get(driver_url, headers=self.headers)
            response.raise_for_status()
            driver_soup = BeautifulSoup(response.text, 'html.parser')
            
            # ドライバーのモデルを取得
            driver_models = driver_soup.select('.product-card')
            for model in driver_models:
                club_data = {
                    'manufacturer': 'Mizuno',
                    'country': 'Japan',
                    'website': self.base_urls['mizuno'],
                    'established_year': 1906,
                    'series': model.select_one('.series-name').text.strip(),
                    'model': model.select_one('.model-name').text.strip(),
                    'club_type': 'driver',
                    'loft_range': model.select_one('.loft-range').text.strip(),
                    'length_range': model.select_one('.length-range').text.strip(),
                    'weight_range': model.select_one('.weight-range').text.strip(),
                    'stock_options': {
                        'shafts': [s.text.strip() for s in model.select('.stock-shafts .shaft')],
                        'grips': [g.text.strip() for g in model.select('.stock-grips .grip')]
                    },
                    'msrp': float(model.select_one('.price').text.strip().replace('¥', '').replace(',', '')),
                    'release_year': int(model.select_one('.release-year').text.strip())
                }
                clubs.append(club_data)
                
            # アイアンのデータを取得
            iron_url = f"{self.base_urls['mizuno']}/golf-clubs/irons"
            response = requests.get(iron_url, headers=self.headers)
            response.raise_for_status()
            iron_soup = BeautifulSoup(response.text, 'html.parser')
            
            # アイアンのモデルを取得
            iron_models = iron_soup.select('.product-card')
            for model in iron_models:
                club_data = {
                    'manufacturer': 'Mizuno',
                    'country': 'Japan',
                    'website': self.base_urls['mizuno'],
                    'established_year': 1906,
                    'series': model.select_one('.series-name').text.strip(),
                    'model': model.select_one('.model-name').text.strip(),
                    'club_type': 'iron',
                    'loft_range': model.select_one('.loft-range').text.strip(),
                    'length_range': model.select_one('.length-range').text.strip(),
                    'weight_range': model.select_one('.weight-range').text.strip(),
                    'stock_options': {
                        'shafts': [s.text.strip() for s in model.select('.stock-shafts .shaft')],
                        'grips': [g.text.strip() for g in model.select('.stock-grips .grip')]
                    },
                    'msrp': float(model.select_one('.price').text.strip().replace('¥', '').replace(',', '')),
                    'release_year': int(model.select_one('.release-year').text.strip())
                }
                clubs.append(club_data)
                
            # ウェッジのデータを取得
            wedge_url = f"{self.base_urls['mizuno']}/golf-clubs/wedges"
            response = requests.get(wedge_url, headers=self.headers)
            response.raise_for_status()
            wedge_soup = BeautifulSoup(response.text, 'html.parser')
            
            # ウェッジのモデルを取得
            wedge_models = wedge_soup.select('.product-card')
            for model in wedge_models:
                club_data = {
                    'manufacturer': 'Mizuno',
                    'country': 'Japan',
                    'website': self.base_urls['mizuno'],
                    'established_year': 1906,
                    'series': model.select_one('.series-name').text.strip(),
                    'model': model.select_one('.model-name').text.strip(),
                    'club_type': 'wedge',
                    'loft_range': model.select_one('.loft-range').text.strip(),
                    'length_range': model.select_one('.length-range').text.strip(),
                    'weight_range': model.select_one('.weight-range').text.strip(),
                    'stock_options': {
                        'shafts': [s.text.strip() for s in model.select('.stock-shafts .shaft')],
                        'grips': [g.text.strip() for g in model.select('.stock-grips .grip')]
                    },
                    'msrp': float(model.select_one('.price').text.strip().replace('¥', '').replace(',', '')),
                    'release_year': int(model.select_one('.release-year').text.strip())
                }
                clubs.append(club_data)
                
            self.logger.info(f"Mizunoから{len(clubs)}件のデータを取得しました。")
            
        except Exception as e:
            self.logger.error(f"Mizunoのスクレイピング中にエラーが発生しました: {str(e)}")
            
        return clubs
        
    def _scrape_srixon(self, soup: BeautifulSoup) -> List[Dict]:
        """Srixonのゴルフクラブデータをスクレイピングします。"""
        clubs = []
        try:
            # ドライバーのデータを取得
            driver_url = f"{self.base_urls['srixon']}/golf-clubs/drivers"
            response = requests.get(driver_url, headers=self.headers)
            response.raise_for_status()
            driver_soup = BeautifulSoup(response.text, 'html.parser')
            
            # ドライバーのモデルを取得
            driver_models = driver_soup.select('.product-card')
            for model in driver_models:
                club_data = {
                    'manufacturer': 'Srixon',
                    'country': 'Japan',
                    'website': self.base_urls['srixon'],
                    'established_year': 1930,
                    'series': model.select_one('.series-name').text.strip(),
                    'model': model.select_one('.model-name').text.strip(),
                    'club_type': 'driver',
                    'loft_range': model.select_one('.loft-range').text.strip(),
                    'length_range': model.select_one('.length-range').text.strip(),
                    'weight_range': model.select_one('.weight-range').text.strip(),
                    'stock_options': {
                        'shafts': [s.text.strip() for s in model.select('.stock-shafts .shaft')],
                        'grips': [g.text.strip() for g in model.select('.stock-grips .grip')]
                    },
                    'msrp': float(model.select_one('.price').text.strip().replace('¥', '').replace(',', '')),
                    'release_year': int(model.select_one('.release-year').text.strip())
                }
                clubs.append(club_data)
                
            # アイアンのデータを取得
            iron_url = f"{self.base_urls['srixon']}/golf-clubs/irons"
            response = requests.get(iron_url, headers=self.headers)
            response.raise_for_status()
            iron_soup = BeautifulSoup(response.text, 'html.parser')
            
            # アイアンのモデルを取得
            iron_models = iron_soup.select('.product-card')
            for model in iron_models:
                club_data = {
                    'manufacturer': 'Srixon',
                    'country': 'Japan',
                    'website': self.base_urls['srixon'],
                    'established_year': 1930,
                    'series': model.select_one('.series-name').text.strip(),
                    'model': model.select_one('.model-name').text.strip(),
                    'club_type': 'iron',
                    'loft_range': model.select_one('.loft-range').text.strip(),
                    'length_range': model.select_one('.length-range').text.strip(),
                    'weight_range': model.select_one('.weight-range').text.strip(),
                    'stock_options': {
                        'shafts': [s.text.strip() for s in model.select('.stock-shafts .shaft')],
                        'grips': [g.text.strip() for g in model.select('.stock-grips .grip')]
                    },
                    'msrp': float(model.select_one('.price').text.strip().replace('¥', '').replace(',', '')),
                    'release_year': int(model.select_one('.release-year').text.strip())
                }
                clubs.append(club_data)
                
            # ウェッジのデータを取得
            wedge_url = f"{self.base_urls['srixon']}/golf-clubs/wedges"
            response = requests.get(wedge_url, headers=self.headers)
            response.raise_for_status()
            wedge_soup = BeautifulSoup(response.text, 'html.parser')
            
            # ウェッジのモデルを取得
            wedge_models = wedge_soup.select('.product-card')
            for model in wedge_models:
                club_data = {
                    'manufacturer': 'Srixon',
                    'country': 'Japan',
                    'website': self.base_urls['srixon'],
                    'established_year': 1930,
                    'series': model.select_one('.series-name').text.strip(),
                    'model': model.select_one('.model-name').text.strip(),
                    'club_type': 'wedge',
                    'loft_range': model.select_one('.loft-range').text.strip(),
                    'length_range': model.select_one('.length-range').text.strip(),
                    'weight_range': model.select_one('.weight-range').text.strip(),
                    'stock_options': {
                        'shafts': [s.text.strip() for s in model.select('.stock-shafts .shaft')],
                        'grips': [g.text.strip() for g in model.select('.stock-grips .grip')]
                    },
                    'msrp': float(model.select_one('.price').text.strip().replace('¥', '').replace(',', '')),
                    'release_year': int(model.select_one('.release-year').text.strip())
                }
                clubs.append(club_data)
                
            self.logger.info(f"Srixonから{len(clubs)}件のデータを取得しました。")
            
        except Exception as e:
            self.logger.error(f"Srixonのスクレイピング中にエラーが発生しました: {str(e)}")
            
        return clubs
        
    def _scrape_cobra(self, soup: BeautifulSoup) -> List[Dict]:
        """Cobraのゴルフクラブデータをスクレイピングします。"""
        clubs = []
        try:
            # ドライバーのデータを取得
            driver_url = f"{self.base_urls['cobra']}/golf-clubs/drivers"
            response = requests.get(driver_url, headers=self.headers)
            response.raise_for_status()
            driver_soup = BeautifulSoup(response.text, 'html.parser')
            
            # ドライバーのモデルを取得
            driver_models = driver_soup.select('.product-card')
            for model in driver_models:
                club_data = {
                    'manufacturer': 'Cobra',
                    'country': 'USA',
                    'website': self.base_urls['cobra'],
                    'established_year': 1973,
                    'series': model.select_one('.series-name').text.strip(),
                    'model': model.select_one('.model-name').text.strip(),
                    'club_type': 'driver',
                    'loft_range': model.select_one('.loft-range').text.strip(),
                    'length_range': model.select_one('.length-range').text.strip(),
                    'weight_range': model.select_one('.weight-range').text.strip(),
                    'stock_options': {
                        'shafts': [s.text.strip() for s in model.select('.stock-shafts .shaft')],
                        'grips': [g.text.strip() for g in model.select('.stock-grips .grip')]
                    },
                    'msrp': float(model.select_one('.price').text.strip().replace('¥', '').replace(',', '')),
                    'release_year': int(model.select_one('.release-year').text.strip())
                }
                clubs.append(club_data)
                
            # アイアンのデータを取得
            iron_url = f"{self.base_urls['cobra']}/golf-clubs/irons"
            response = requests.get(iron_url, headers=self.headers)
            response.raise_for_status()
            iron_soup = BeautifulSoup(response.text, 'html.parser')
            
            # アイアンのモデルを取得
            iron_models = iron_soup.select('.product-card')
            for model in iron_models:
                club_data = {
                    'manufacturer': 'Cobra',
                    'country': 'USA',
                    'website': self.base_urls['cobra'],
                    'established_year': 1973,
                    'series': model.select_one('.series-name').text.strip(),
                    'model': model.select_one('.model-name').text.strip(),
                    'club_type': 'iron',
                    'loft_range': model.select_one('.loft-range').text.strip(),
                    'length_range': model.select_one('.length-range').text.strip(),
                    'weight_range': model.select_one('.weight-range').text.strip(),
                    'stock_options': {
                        'shafts': [s.text.strip() for s in model.select('.stock-shafts .shaft')],
                        'grips': [g.text.strip() for g in model.select('.stock-grips .grip')]
                    },
                    'msrp': float(model.select_one('.price').text.strip().replace('¥', '').replace(',', '')),
                    'release_year': int(model.select_one('.release-year').text.strip())
                }
                clubs.append(club_data)
                
            # ウェッジのデータを取得
            wedge_url = f"{self.base_urls['cobra']}/golf-clubs/wedges"
            response = requests.get(wedge_url, headers=self.headers)
            response.raise_for_status()
            wedge_soup = BeautifulSoup(response.text, 'html.parser')
            
            # ウェッジのモデルを取得
            wedge_models = wedge_soup.select('.product-card')
            for model in wedge_models:
                club_data = {
                    'manufacturer': 'Cobra',
                    'country': 'USA',
                    'website': self.base_urls['cobra'],
                    'established_year': 1973,
                    'series': model.select_one('.series-name').text.strip(),
                    'model': model.select_one('.model-name').text.strip(),
                    'club_type': 'wedge',
                    'loft_range': model.select_one('.loft-range').text.strip(),
                    'length_range': model.select_one('.length-range').text.strip(),
                    'weight_range': model.select_one('.weight-range').text.strip(),
                    'stock_options': {
                        'shafts': [s.text.strip() for s in model.select('.stock-shafts .shaft')],
                        'grips': [g.text.strip() for g in model.select('.stock-grips .grip')]
                    },
                    'msrp': float(model.select_one('.price').text.strip().replace('¥', '').replace(',', '')),
                    'release_year': int(model.select_one('.release-year').text.strip())
                }
                clubs.append(club_data)
                
            self.logger.info(f"Cobraから{len(clubs)}件のデータを取得しました。")
            
        except Exception as e:
            self.logger.error(f"Cobraのスクレイピング中にエラーが発生しました: {str(e)}")
            
        return clubs
        
    def _scrape_honma(self, soup: BeautifulSoup) -> List[Dict]:
        """Honmaのゴルフクラブデータをスクレイピングします。"""
        clubs = []
        try:
            # ドライバーのデータを取得
            driver_url = f"{self.base_urls['honma']}/golf-clubs/drivers"
            response = requests.get(driver_url, headers=self.headers)
            response.raise_for_status()
            driver_soup = BeautifulSoup(response.text, 'html.parser')
            
            # ドライバーのモデルを取得
            driver_models = driver_soup.select('.product-card')
            for model in driver_models:
                club_data = {
                    'manufacturer': 'Honma',
                    'country': 'Japan',
                    'website': self.base_urls['honma'],
                    'established_year': 1959,
                    'series': model.select_one('.series-name').text.strip(),
                    'model': model.select_one('.model-name').text.strip(),
                    'club_type': 'driver',
                    'loft_range': model.select_one('.loft-range').text.strip(),
                    'length_range': model.select_one('.length-range').text.strip(),
                    'weight_range': model.select_one('.weight-range').text.strip(),
                    'stock_options': {
                        'shafts': [s.text.strip() for s in model.select('.stock-shafts .shaft')],
                        'grips': [g.text.strip() for g in model.select('.stock-grips .grip')]
                    },
                    'msrp': float(model.select_one('.price').text.strip().replace('¥', '').replace(',', '')),
                    'release_year': int(model.select_one('.release-year').text.strip())
                }
                clubs.append(club_data)
                
            # アイアンのデータを取得
            iron_url = f"{self.base_urls['honma']}/golf-clubs/irons"
            response = requests.get(iron_url, headers=self.headers)
            response.raise_for_status()
            iron_soup = BeautifulSoup(response.text, 'html.parser')
            
            # アイアンのモデルを取得
            iron_models = iron_soup.select('.product-card')
            for model in iron_models:
                club_data = {
                    'manufacturer': 'Honma',
                    'country': 'Japan',
                    'website': self.base_urls['honma'],
                    'established_year': 1959,
                    'series': model.select_one('.series-name').text.strip(),
                    'model': model.select_one('.model-name').text.strip(),
                    'club_type': 'iron',
                    'loft_range': model.select_one('.loft-range').text.strip(),
                    'length_range': model.select_one('.length-range').text.strip(),
                    'weight_range': model.select_one('.weight-range').text.strip(),
                    'stock_options': {
                        'shafts': [s.text.strip() for s in model.select('.stock-shafts .shaft')],
                        'grips': [g.text.strip() for g in model.select('.stock-grips .grip')]
                    },
                    'msrp': float(model.select_one('.price').text.strip().replace('¥', '').replace(',', '')),
                    'release_year': int(model.select_one('.release-year').text.strip())
                }
                clubs.append(club_data)
                
            # ウェッジのデータを取得
            wedge_url = f"{self.base_urls['honma']}/golf-clubs/wedges"
            response = requests.get(wedge_url, headers=self.headers)
            response.raise_for_status()
            wedge_soup = BeautifulSoup(response.text, 'html.parser')
            
            # ウェッジのモデルを取得
            wedge_models = wedge_soup.select('.product-card')
            for model in wedge_models:
                club_data = {
                    'manufacturer': 'Honma',
                    'country': 'Japan',
                    'website': self.base_urls['honma'],
                    'established_year': 1959,
                    'series': model.select_one('.series-name').text.strip(),
                    'model': model.select_one('.model-name').text.strip(),
                    'club_type': 'wedge',
                    'loft_range': model.select_one('.loft-range').text.strip(),
                    'length_range': model.select_one('.length-range').text.strip(),
                    'weight_range': model.select_one('.weight-range').text.strip(),
                    'stock_options': {
                        'shafts': [s.text.strip() for s in model.select('.stock-shafts .shaft')],
                        'grips': [g.text.strip() for g in model.select('.stock-grips .grip')]
                    },
                    'msrp': float(model.select_one('.price').text.strip().replace('¥', '').replace(',', '')),
                    'release_year': int(model.select_one('.release-year').text.strip())
                }
                clubs.append(club_data)
                
            self.logger.info(f"Honmaから{len(clubs)}件のデータを取得しました。")
            
        except Exception as e:
            self.logger.error(f"Honmaのスクレイピング中にエラーが発生しました: {str(e)}")
            
        return clubs
        
    def save_to_database(self, clubs: List[Dict]) -> bool:
        """取得したデータをデータベースに保存します。"""
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            
            for club in clubs:
                # メーカーテーブルへの挿入
                cursor.execute("""
                    INSERT OR IGNORE INTO manufacturers (
                        name, country, website, established_year
                    ) VALUES (?, ?, ?, ?)
                """, (
                    club['manufacturer'],
                    club['country'],
                    club['website'],
                    club['established_year']
                ))
                
                # シリーズテーブルへの挿入
                cursor.execute("""
                    INSERT OR IGNORE INTO series (
                        manufacturer_id, name, release_year, target_handicap_range
                    ) VALUES (
                        (SELECT id FROM manufacturers WHERE name = ?),
                        ?, ?, ?
                    )
                """, (
                    club['manufacturer'],
                    club['series'],
                    club['release_year'],
                    club['target_handicap_range']
                ))
                
                # モデルテーブルへの挿入
                cursor.execute("""
                    INSERT OR IGNORE INTO models (
                        series_id, name, club_type, loft_range, length_range,
                        weight_range, stock_options, msrp, release_year
                    ) VALUES (
                        (SELECT id FROM series WHERE name = ?),
                        ?, ?, ?, ?, ?, ?, ?, ?
                    )
                """, (
                    club['series'],
                    club['model'],
                    club['club_type'],
                    club['loft_range'],
                    club['length_range'],
                    club['weight_range'],
                    json.dumps(club['stock_options']),
                    club['msrp'],
                    club['release_year']
                ))
                
            conn.commit()
            self.logger.info(f"{len(clubs)}件のデータをデータベースに保存しました。")
            return True
            
        except Exception as e:
            self.logger.error(f"データベースへの保存中にエラーが発生しました: {str(e)}")
            return False
            
    def run(self):
        """スクレイピングを実行します。"""
        try:
            for manufacturer in self.base_urls.keys():
                clubs = self.fetch_manufacturer_data(manufacturer)
                if clubs:
                    self.save_to_database(clubs)
                time.sleep(5)  # サーバーへの負荷を考慮して待機
                
        except Exception as e:
            self.logger.error(f"スクレイピングの実行中にエラーが発生しました: {str(e)}")
            raise

def main():
    """メイン関数です。"""
    # ロギングの設定
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # スクレイパーの初期化と実行
        scraper = GolfClubScraper()
        scraper.run()
        
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        raise
    finally:
        # データベース接続のクローズ
        DatabaseConnection.close_connection()
        logger.info("データベース接続を閉じました。")

if __name__ == "__main__":
    main() 