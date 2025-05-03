import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json
import os
from typing import Dict, List, Optional
import re
import logging

# ロギングの設定
logging.basicConfig(
    level=logging.DEBUG,  # デバッグレベルに変更
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping.log'),
        logging.StreamHandler()
    ]
)

class TitleistDriverScraper:
    def __init__(self):
        self.base_url = "https://golfnavi.info"
        self.drivers_url = f"{self.base_url}/driver"  # URLを修正
        self.params = {
            "cat_id": "21",  # ドライバーカテゴリ
            "maker": "53",   # タイトリストメーカーID
        }

    async def get_driver_data(self) -> List[Dict]:
        async with async_playwright() as p:
            # ブラウザの設定を調整
            browser = await p.chromium.launch(
                headless=True,
                args=['--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage']
            )
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
            )
            page = await context.new_page()

            try:
                # 直接ドライバーページにアクセス
                logging.info(f"ドライバーページにアクセス: {self.drivers_url}")
                
                response = await page.goto(self.drivers_url, wait_until="networkidle", timeout=90000)
                if not response or response.status != 200:
                    logging.error(f"ドライバーページへのアクセスに失敗しました: {response.status if response else 'No response'}")
                    # レスポンスの詳細をログに記録
                    if response:
                        logging.debug(f"レスポンスヘッダー: {response.headers}")
                    return []
                
                # ページの内容を確認
                html = await page.content()
                logging.debug(f"ページの内容: {html[:2000]}")  # 最初の2000文字を表示
                
                # スクリーンショットを保存（デバッグ用）
                await page.screenshot(path="debug_screenshot.png")
                logging.info("デバッグ用スクリーンショットを保存しました")
                
                soup = BeautifulSoup(html, 'html.parser')
                
                # 商品リストを取得（複数のクラスを試す）
                product_list = soup.find_all(['div', 'article'], class_=['product-item', 'item', 'product', 'club-item'])
                if not product_list:
                    logging.error("商品リストが見つかりませんでした。")
                    logging.debug(f"ページの内容: {soup.prettify()[:2000]}")
                    return []

                logging.info(f"商品数: {len(product_list)}")
                drivers = []

                # 各商品を処理
                for idx, product in enumerate(product_list, 1):
                    try:
                        # 商品名を取得
                        name_elem = product.find(['h3', 'h2', 'h4', 'a'], class_=['product-name', 'name', 'title', 'club-name'])
                        if not name_elem:
                            logging.warning(f"商品 {idx} の名前が見つかりませんでした")
                            continue
                        
                        product_name = name_elem.get_text(strip=True)
                        product_link = name_elem.find('a', href=True) if name_elem.name != 'a' else name_elem
                        product_url = f"{self.base_url}{product_link['href']}" if product_link and 'href' in product_link.attrs else ""
                        
                        # スペック情報を取得
                        specs = product.find_all(['dl', 'div', 'table'], class_=['spec-item', 'spec', 'detail', 'club-spec'])
                        spec_dict = {}
                        for spec in specs:
                            dt = spec.find(['dt', 'span', 'div', 'th'], class_=['label', 'title', 'spec-name'])
                            dd = spec.find(['dd', 'span', 'div', 'td'], class_=['value', 'content', 'spec-value'])
                            if dt and dd:
                                spec_dict[dt.get_text(strip=True)] = dd.get_text(strip=True)
                        
                        # 発売日を取得
                        release_date = spec_dict.get("発売日", "")
                        
                        driver_data = {
                            "セットID": "",
                            "セット名": product_name,
                            "ブランド名": "Titleist",
                            "モデル年": release_date[:4] if release_date else "",
                            "参考価格": spec_dict.get("価格", ""),
                            "対象ユーザー層": "",
                            "セットの特徴・コンセプト": "",
                            "推奨度": "",
                            "クラブ種別": "ドライバー",
                            "クラブ名": product_name,
                            "ロフト角": spec_dict.get("ロフト角", ""),
                            "シャフト名・素材": spec_dict.get("シャフト", ""),
                            "フレックス": spec_dict.get("フレックス", ""),
                            "長さ": spec_dict.get("長さ", ""),
                            "ライ角": spec_dict.get("ライ角", ""),
                            "クラブ重量": spec_dict.get("重量", ""),
                            "ヘッド素材": spec_dict.get("ヘッド素材", ""),
                            "シャフト重量": spec_dict.get("シャフト重量", ""),
                            "グリップ名": spec_dict.get("グリップ", ""),
                            "単品価格": spec_dict.get("価格", ""),
                            "ブランドロゴ画像ファイル名": "titleist.svg",
                            "発売日": release_date,
                            "公式商品ページURL": product_url,
                            "商品画像URL": "",
                            "備考": ""
                        }
                        drivers.append(driver_data)
                        logging.info(f"商品 {idx} のデータを取得しました: {product_name}")
                        
                    except Exception as e:
                        logging.error(f"商品 {idx} の処理中にエラーが発生しました: {str(e)}")
                        continue
                
                return drivers
                
            except Exception as e:
                logging.error(f"スクレイピング中にエラーが発生しました: {str(e)}")
                return []
            
            finally:
                await browser.close()

async def main():
    scraper = TitleistDriverScraper()
    drivers = await scraper.get_driver_data()
    
    if not drivers:
        logging.error("ドライバーのデータを取得できませんでした。")
        return

    # データをDataFrameに変換
    df = pd.DataFrame(drivers)
    
    # 現在の日時をファイル名に使用
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"titleist_drivers_{timestamp}.csv"
    
    # CSVファイルとして保存
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    logging.info(f"データを {output_file} に保存しました。")

if __name__ == "__main__":
    asyncio.run(main()) 