import requests
from bs4 import BeautifulSoup
import logging
import time
import json
import re
from typing import Dict, List, Optional
from pathlib import Path

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class GolfNaviScraper:
    def __init__(self):
        self.base_url = "https://golfnavi.info"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
        # 主要メーカー一覧
        self.manufacturers = [
            {
                'name': 'テーラーメイド',
                'url': f"{self.base_url}/club-cate/taylormade"
            },
            {
                'name': 'キャロウェイ',
                'url': f"{self.base_url}/club-cate/callaway"
            },
            {
                'name': 'タイトリスト',
                'url': f"{self.base_url}/club-cate/titleist"
            },
            {
                'name': 'ピン',
                'url': f"{self.base_url}/club-cate/ping"
            },
            {
                'name': 'ミズノ',
                'url': f"{self.base_url}/club-cate/mizuno"
            },
            {
                'name': 'コブラ',
                'url': f"{self.base_url}/club-cate/cobra"
            },
            {
                'name': 'ブリヂストン',
                'url': f"{self.base_url}/club-cate/bridgestone"
            },
            {
                'name': 'ダンロップ',
                'url': f"{self.base_url}/club-cate/dunlop"
            },
            {
                'name': 'ホンma',
                'url': f"{self.base_url}/club-cate/honma"
            },
            {
                'name': 'XXIO',
                'url': f"{self.base_url}/club-cate/xxio"
            }
        ]

    def fetch_page(self, url):
        """ページを取得する"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logging.error(f"ページの取得に失敗しました: {url} - {str(e)}")
            return None

    def extract_specs(self, text):
        """テキストからスペック情報を抽出する"""
        specs = {}
        
        # ロフト角
        loft_match = re.search(r'ロフト[：:]\s*([0-9.]+)\s*度', text)
        if loft_match:
            specs['loft'] = float(loft_match.group(1))
        
        # 長さ
        length_match = re.search(r'長さ[：:]\s*([0-9.]+)\s*インチ', text)
        if length_match:
            specs['length'] = float(length_match.group(1))
        
        # 重量
        weight_match = re.search(r'重量[：:]\s*([0-9.]+)\s*g', text)
        if weight_match:
            specs['weight'] = float(weight_match.group(1))
        
        # フレックス
        flex_match = re.search(r'フレックス[：:]\s*([A-Z]+)', text)
        if flex_match:
            specs['flex'] = flex_match.group(1)
        
        # シャフト
        shaft_match = re.search(r'シャフト[：:]\s*([^\n]+)', text)
        if shaft_match:
            specs['shaft'] = shaft_match.group(1).strip()
        
        # グリップ
        grip_match = re.search(r'グリップ[：:]\s*([^\n]+)', text)
        if grip_match:
            specs['grip'] = grip_match.group(1).strip()
        
        # 価格
        price_match = re.search(r'価格[：:]\s*([0-9,]+)\s*円', text)
        if price_match:
            specs['price'] = int(price_match.group(1).replace(',', ''))
        
        return specs

    def get_club_info(self, url):
        """クラブ情報を取得する"""
        html = self.fetch_page(url)
        if not html:
            return []

        soup = BeautifulSoup(html, 'html.parser')
        clubs = []

        # 記事を探す
        for article in soup.find_all('article'):
            try:
                # タイトルを取得
                title_elem = article.find('h1', class_='entry-title')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                logging.info(f"クラブ情報を解析中: {title}")

                # 仕様情報を取得
                content = article.find('div', class_='entry-content')
                if content:
                    text = content.get_text()
                    specs = self.extract_specs(text)
                    
                    # クラブタイプを判定
                    club_type = None
                    if 'ドライバー' in title:
                        club_type = 'driver'
                    elif 'アイアン' in title:
                        club_type = 'iron'
                    elif 'ウェッジ' in title:
                        club_type = 'wedge'
                    elif 'フェアウェイウッド' in title:
                        club_type = 'fairway_wood'
                    elif 'ユーティリティ' in title:
                        club_type = 'utility'
                    elif 'パター' in title:
                        club_type = 'putter'

                    clubs.append({
                        'title': title,
                        'type': club_type,
                        'specs': specs
                    })
                    logging.info(f"クラブ情報を追加: {title}")

            except Exception as e:
                logging.error(f"クラブ情報の解析中にエラーが発生しました: {str(e)}")
                continue

        return clubs

    def save_data(self, data, filename):
        """データをJSONファイルとして保存する"""
        try:
            with open(self.data_dir / filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logging.info(f"データを保存しました: {filename}")
        except Exception as e:
            logging.error(f"データの保存に失敗しました: {str(e)}")

    def run(self):
        """スクレイピングを実行する"""
        # メーカー一覧を保存
        self.save_data(self.manufacturers, 'manufacturers.json')

        # 各メーカーのクラブ情報を取得
        all_clubs = []
        for manufacturer in self.manufacturers:
            try:
                clubs = self.get_club_info(manufacturer['url'])
                all_clubs.extend(clubs)
                logging.info(f"{manufacturer['name']}から{len(clubs)}件のクラブ情報を取得")
                time.sleep(1)  # サーバー負荷軽減のため
            except Exception as e:
                logging.error(f"{manufacturer['name']}のクラブ情報取得中にエラーが発生しました: {str(e)}")
                continue

        self.save_data(all_clubs, 'clubs.json')
        logging.info(f"合計{len(all_clubs)}件のクラブ情報を取得しました")

if __name__ == "__main__":
    scraper = GolfNaviScraper()
    scraper.run() 