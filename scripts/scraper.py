import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
from typing import List, Dict
import re
from requests.exceptions import RequestException, Timeout
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from sqlalchemy.orm import Session
from app.models import Product, PriceHistory
from datetime import datetime
from app.scraper_utils import ScraperUtils, retry_on_failure
from app.slack_notifier import SlackNotifier
import os
import sys
import logging
from config import (
    SCRAPING_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY,
    LOG_LEVEL,
    LOG_FILE,
    SLACK_WEBHOOK_URL
)
from pathlib import Path

# プロジェクトのルートディレクトリを取得
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from scripts.slack_notifier import send_slack_notification

# ログ設定
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def print_progress(current: int, total: int, prefix: str = '', suffix: str = ''):
    """進捗状況を表示"""
    bar_length = 50
    filled_length = int(round(bar_length * current / float(total)))
    percents = round(100.0 * current / float(total), 1)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\r{prefix} [{bar}] {percents}% {suffix}')
    sys.stdout.flush()
    if current == total:
        print()

class GolfClubScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        self.timeout = 30
        self.base_urls = {
            "fujikura": "https://www.fujikurashaft.jp/library/",
            "ping_products": "https://clubping.jp/product/",
            "golfdigest": "https://lesson.golfdigest.co.jp/gear/topics/article/161126/1/",
            "masa_golf_ranking": "https://www.masa-golf.jp/article/455463138.html",
            "masa_golf_ironshaft": "https://www.masa-golf.jp/ironshaftosusume",
            "a_golf_shaft": "https://www.a-golf.net/f/content/golfclub-shaft.html",
            "a_golf_driver": "https://www.a-golf.net/f/content/driver-shaft.html",
            "golfclub_shop": "https://golfclub.co.jp/driver-shaft/"
        }
        
        # Seleniumの設定
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument(f'user-agent={self.headers["User-Agent"]}')
        
        self.driver = None
        self.slack = SlackNotifier(SLACK_WEBHOOK_URL) if SLACK_WEBHOOK_URL else None
        self.retry_count = 0
        self.data_dir = project_root / 'data'
        self.data_dir.mkdir(exist_ok=True)

    def setup_driver(self):
        """Chromeドライバーのセットアップ"""
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.driver.set_page_load_timeout(SCRAPING_TIMEOUT)
            self.driver.implicitly_wait(10)
            self.utils = ScraperUtils(self.driver)
            logger.info("Chromeドライバーの初期化に成功しました")
        except Exception as e:
            error_msg = f"Chromeドライバーの初期化に失敗しました: {str(e)}"
            logger.error(error_msg)
            if self.slack:
                self.slack.notify_error(e, {"context": "ドライバー初期化"})
            raise

    def retry_on_failure(self, func, *args, **kwargs):
        """失敗時のリトライ処理"""
        while self.retry_count < MAX_RETRIES:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.retry_count += 1
                error_msg = f"エラーが発生しました（リトライ {self.retry_count}/{MAX_RETRIES}）: {str(e)}"
                logger.warning(error_msg)
                if self.slack:
                    self.slack.notify_error(e, {"context": "リトライ処理"})
                
                if self.retry_count < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)
                    continue
                else:
                    error_msg = f"最大リトライ回数に達しました: {str(e)}"
                    logger.error(error_msg)
                    if self.slack:
                        self.slack.notify_error(e, {"context": "最大リトライ"})
                    raise

    def wait_for_element(self, by, value, timeout=SCRAPING_TIMEOUT):
        """要素の出現を待機"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            error_msg = f"要素が見つかりません: {value}"
            logger.error(error_msg)
            if self.slack:
                self.slack.notify_error(TimeoutException(error_msg), {"context": "要素待機"})
            raise

    def scrape_fujikura(self) -> List[Dict]:
        """フジクラシャフトの情報をスクレイピング"""
        try:
            if self.slack:
                self.slack.notify_scraping_start("フジクラシャフト")
            
            logger.info("フジクラシャフトのスクレイピングを開始")
            self.driver.get(self.base_urls['fujikura'])
            
            # ページ読み込み完了を待機
            self.utils.wait_for_page_load()
            
            # テーブルが表示されるまで明示的に待機
            tables = WebDriverWait(self.driver, SCRAPING_TIMEOUT).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table.res_table'))
            )
            
            shafts = []
            total_tables = len(tables)
            logger.info(f"テーブル数: {total_tables}")
            
            for table_idx, table in enumerate(tables, 1):
                print_progress(table_idx, total_tables, prefix='テーブル処理中:', suffix=f'({table_idx}/{total_tables})')
                
                try:
                    # テーブルの行を取得
                    rows = WebDriverWait(table, 10).until(
                        EC.presence_of_all_elements_located((By.TAG_NAME, 'tr'))
                    )
                    
                    if len(rows) <= 1:
                        logger.warning(f"テーブル {table_idx} はデータが不足しています")
                        continue
                    
                    current_model = ""
                    current_series = ""
                    header_cells = rows[0].find_elements(By.TAG_NAME, 'th')
                    header_texts = [cell.text.strip() for cell in header_cells]
                    
                    for row_idx, row in enumerate(rows[1:], 1):
                        try:
                            cells = row.find_elements(By.TAG_NAME, 'td')
                            model_text = self.utils.safe_get_text(cells[0])
                            
                            # シリーズ名とモデル名の処理
                            if model_text:
                                if "シリーズ" in model_text:
                                    current_series = model_text.replace("シリーズ", "").strip()
                                    continue
                                else:
                                    current_model = model_text
                            
                            # シャフトデータの構築
                            shaft = {
                                "brand": "Fujikura",
                                "series": current_series,
                                "model": current_model,
                                "type": "shaft",
                                "url": self.base_urls['fujikura'],
                                "scraping_date": datetime.now().isoformat(),
                            }
                            
                            # 各セルのデータを追加
                            for idx, (header, cell) in enumerate(zip(header_texts[1:], cells[1:]), 1):
                                value = self.utils.safe_get_text(cell)
                                key = header.lower().replace(" ", "_")
                                shaft[key] = value
                            
                            # データの検証
                            required_fields = ["model", "flex", "weight"]
                            if all(shaft.get(field) for field in required_fields):
                                # 数値データの正規化
                                for field in ["weight", "length", "torque"]:
                                    if field in shaft and shaft[field]:
                                        try:
                                            shaft[field] = float(re.sub(r'[^\d.]', '', shaft[field]))
                                        except ValueError:
                                            logger.warning(f"数値変換エラー: {field}={shaft[field]}")
                                
                                # 価格の正規化
                                if "price" in shaft and shaft["price"]:
                                    price_match = re.search(r'¥([\d,]+)', shaft["price"])
                                    if price_match:
                                        shaft["price"] = int(price_match.group(1).replace(',', ''))
                                
                                shafts.append(shaft)
                            else:
                                logger.warning(f"必須フィールドが不足: {shaft}")
                            
                        except Exception as e:
                            logger.error(f"行 {row_idx} の処理でエラー: {str(e)}")
                            if self.slack:
                                self.slack.notify_error(e, {
                                    "context": "フジクラシャフト行処理",
                                    "table": table_idx,
                                    "row": row_idx
                                })
                            continue
                
                except Exception as e:
                    logger.error(f"テーブル {table_idx} の処理でエラー: {str(e)}")
                    if self.slack:
                        self.slack.notify_error(e, {
                            "context": "フジクラシャフトテーブル処理",
                            "table": table_idx
                        })
                    continue
            
            logger.info(f"フジクラシャフトのスクレイピングが完了。{len(shafts)}件のデータを取得")
            if self.slack:
                self.slack.notify_scraping_complete("フジクラシャフト", len(shafts))
            
            return shafts
            
        except Exception as e:
            error_msg = f"フジクラシャフトのスクレイピングでエラー: {str(e)}"
            logger.error(error_msg)
            if self.slack:
                self.slack.notify_error(e, {"context": "フジクラシャフトスクレイピング"})
            raise

    def scrape_ping(self) -> List[Dict]:
        """PINGのニュースデータをスクレイピング"""
        try:
            response = requests.get(self.base_urls["ping"], headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            news_items = []
            
            # ニュース情報の取得（セレクタを修正）
            news_elements = soup.select('article.news-item')  # 修正
            for element in news_elements:
                try:
                    news = {
                        "brand": "PING",
                        "title": element.select_one('h2').text.strip(),  # 修正
                        "date": element.select_one('time').text.strip() if element.select_one('time') else "",  # 修正
                        "content": element.select_one('div.content').text.strip() if element.select_one('div.content') else ""  # 修正
                    }
                    news_items.append(news)
                except Exception as e:
                    print(f"ニュースデータの処理でエラー: {str(e)}")
                    continue
            
            return news_items
        except Exception as e:
            print(f"PINGニュースのスクレイピングでエラー: {str(e)}")
            return []

    def scrape_golfdigest(self) -> List[Dict]:
        """ゴルフダイジェストのギア比較データをスクレイピング"""
        try:
            if self.slack:
                self.slack.notify_scraping_start("ゴルフダイジェスト")
            
            logger.info("ゴルフダイジェストのスクレイピングを開始")
            self.driver.get(self.base_urls['golfdigest'])
            
            # ページ読み込み完了を待機
            self.utils.wait_for_page_load()
            
            gear_items = []
            
            try:
                # ギア比較情報の取得
                gear_elements = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.gear-comparison-item"))
                )
                logger.info(f"ギア比較項目数: {len(gear_elements)}")
                
                for idx, element in enumerate(gear_elements, 1):
                    try:
                        logger.info(f"ギア情報処理開始: {idx}/{len(gear_elements)}")
                        
                        gear = {
                            "brand": self.utils.safe_get_text(element, "span.brand"),
                            "model": self.utils.safe_get_text(element, "h3"),
                            "type": self.utils.safe_get_text(element, "span.type"),
                            "features": [],
                            "scraping_date": datetime.now().isoformat()
                        }
                        
                        # 価格情報の取得と正規化
                        price_text = self.utils.safe_get_text(element, "span.price")
                        if price_text:
                            price_match = re.search(r'¥([\d,]+)', price_text)
                            if price_match:
                                gear["price"] = int(price_match.group(1).replace(',', ''))
                                gear["is_tax_included"] = "税込" in price_text
                        
                        # 特徴情報の取得
                        features = element.find_elements(By.CSS_SELECTOR, "div.features p")
                        gear["features"] = [f.text.strip() for f in features if f.text.strip()]
                        
                        # 評価情報の取得
                        rating = self.utils.safe_get_text(element, "span.rating")
                        if rating:
                            try:
                                gear["rating"] = float(rating)
                            except ValueError:
                                logger.warning(f"評価値の変換に失敗: {rating}")
                        
                        # 必須フィールドのチェック
                        required_fields = ["brand", "model", "type"]
                        if all(gear.get(field) for field in required_fields):
                            gear_items.append(gear)
                            logger.info(f"ギア情報を取得: {gear['brand']} - {gear['model']}")
                        else:
                            logger.warning(f"必須フィールドが不足: {gear}")
                            
                    except Exception as e:
                        logger.error(f"ギア情報の取得に失敗: {str(e)}")
                        if self.slack:
                            self.slack.notify_error(e, {
                                "context": "ゴルフダイジェストギア情報取得",
                                "index": idx
                            })
                        continue
                
            except Exception as e:
                logger.error(f"ギア比較情報の取得に失敗: {str(e)}")
                if self.slack:
                    self.slack.notify_error(e, {"context": "ゴルフダイジェストギア比較取得"})
                return gear_items
            
            logger.info(f"ゴルフダイジェストのスクレイピングが完了。{len(gear_items)}件のデータを取得")
            if self.slack:
                self.slack.notify_scraping_complete("ゴルフダイジェスト", len(gear_items))
            
            return gear_items
            
        except Exception as e:
            error_msg = f"ゴルフダイジェストのスクレイピングでエラー: {str(e)}"
            logger.error(error_msg)
            if self.slack:
                self.slack.notify_error(e, {"context": "ゴルフダイジェストスクレイピング"})
            raise

    def scrape_masa_golf_ranking(self) -> List[Dict]:
        """マサゴルフのシャフトランキングデータをスクレイピング"""
        try:
            if self.slack:
                self.slack.notify_scraping_start("マサゴルフランキング")
            
            logger.info("マサゴルフランキングのスクレイピングを開始")
            self.driver.get(self.base_urls['masa_golf_ranking'])
            
            # ページ読み込み完了を待機
            self.utils.wait_for_page_load()
            
            rankings = []
            
            try:
                # ランキング情報の取得
                rank_elements = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.ranking-item"))
                )
                logger.info(f"ランキング項目数: {len(rank_elements)}")
                
                for idx, element in enumerate(rank_elements, 1):
                    try:
                        logger.info(f"ランキング情報処理開始: {idx}/{len(rank_elements)}")
                        
                        rank = {
                            "rank": self.utils.safe_get_text(element, "span.rank"),
                            "brand": self.utils.safe_get_text(element, "span.brand"),
                            "model": self.utils.safe_get_text(element, "h3"),
                            "type": "shaft",
                            "features": [],
                            "scraping_date": datetime.now().isoformat()
                        }
                        
                        # 特徴情報の取得
                        features = element.find_elements(By.CSS_SELECTOR, "div.features p")
                        rank["features"] = [f.text.strip() for f in features if f.text.strip()]
                        
                        # 評価情報の取得
                        rating = self.utils.safe_get_text(element, "span.rating")
                        if rating:
                            try:
                                rank["rating"] = float(rating)
                            except ValueError:
                                logger.warning(f"評価値の変換に失敗: {rating}")
                        
                        # 必須フィールドのチェック
                        required_fields = ["rank", "brand", "model"]
                        if all(rank.get(field) for field in required_fields):
                            rankings.append(rank)
                            logger.info(f"ランキング情報を取得: {rank['rank']}位 - {rank['brand']} - {rank['model']}")
                        else:
                            logger.warning(f"必須フィールドが不足: {rank}")
                            
                    except Exception as e:
                        logger.error(f"ランキング情報の取得に失敗: {str(e)}")
                        if self.slack:
                            self.slack.notify_error(e, {
                                "context": "マサゴルフランキング情報取得",
                                "index": idx
                            })
                        continue
                
            except Exception as e:
                logger.error(f"ランキング情報の取得に失敗: {str(e)}")
                if self.slack:
                    self.slack.notify_error(e, {"context": "マサゴルフランキング取得"})
                return rankings
            
            logger.info(f"マサゴルフランキングのスクレイピングが完了。{len(rankings)}件のデータを取得")
            if self.slack:
                self.slack.notify_scraping_complete("マサゴルフランキング", len(rankings))
            
            return rankings
            
        except Exception as e:
            error_msg = f"マサゴルフランキングのスクレイピングでエラー: {str(e)}"
            logger.error(error_msg)
            if self.slack:
                self.slack.notify_error(e, {"context": "マサゴルフランキングスクレイピング"})
            raise

    def scrape_ping_news(self):
        print("PINGニュースの収集を開始します...")
        url = "https://clubping.jp/news/"
        print(f"アクセスするURL: {url}")
        
        try:
            self.driver.get(url)
            print("ページにアクセスしました")
            
            # ページの読み込みを待機
            time.sleep(5)
            print("ページの読み込みを待機しました")
            
            # HTMLの構造を保存（デバッグ用）
            with open("ping_debug.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            print("HTMLの構造を保存しました")
            
            # ニュース記事を取得
            news_items = self.driver.find_elements(By.CSS_SELECTOR, "div.newsArea article")
            print(f"ニュース記事数: {len(news_items)}")
            
            results = []
            for item in news_items:
                try:
                    title = item.find_element(By.CSS_SELECTOR, "h2").text
                    date = item.find_element(By.CSS_SELECTOR, "time").text
                    content = item.find_element(By.CSS_SELECTOR, "div.txt").text
                    
                    result = {
                        "title": title,
                        "date": date,
                        "content": content
                    }
                    results.append(result)
                    print(f"ニュース記事を追加: {title}")
                except Exception as e:
                    print(f"記事の処理でエラー: {str(e)}")
                    continue
            
            return results
        except Exception as e:
            print(f"PINGニュースのスクレイピングでエラー: {str(e)}")
            return []

    def scrape_ping_products(self) -> List[Dict]:
        """PING製品の情報をスクレイピング"""
        try:
            if self.slack:
                self.slack.notify_scraping_start("PING製品")
            
            logger.info("PING製品のスクレイピングを開始")
            self.driver.get(self.base_urls['ping_products'])
            
            # ページ読み込み完了を待機
            self.utils.wait_for_page_load()
            
            products = []
            
            # カテゴリーリンクを取得
            category_links = []
            try:
                category_elements = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.sidemenu_frame li.slidemenu a"))
                )
                for category in category_elements[:3]:  # テスト用に3カテゴリーに制限
                    category_links.append({
                        "name": category.text.strip(),
                        "url": category.get_attribute("href")
                    })
                logger.info(f"カテゴリー数: {len(category_links)}")
            except Exception as e:
                logger.error(f"カテゴリーリンクの取得に失敗: {str(e)}")
                if self.slack:
                    self.slack.notify_error(e, {"context": "PINGカテゴリー取得"})
                return products
            
            # カテゴリーごとに処理
            for category_idx, category in enumerate(category_links, 1):
                try:
                    logger.info(f"カテゴリー処理開始: {category['name']} ({category_idx}/{len(category_links)})")
                    
                    # カテゴリーページに移動
                    self.driver.get(category["url"])
                    self.utils.wait_for_page_load()
                    
                    # 製品リンクを取得
                    product_links = []
                    try:
                        product_elements = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.sidemenu_frame li.slidemenu ul li a"))
                        )
                        for element in product_elements[:3]:  # テスト用に3製品に制限
                            product_links.append({
                                "name": element.text.strip(),
                                "url": element.get_attribute("href")
                            })
                    except Exception as e:
                        logger.error(f"製品リンクの取得に失敗: {str(e)}")
                        continue
                    
                    # 製品ごとに処理
                    for product_idx, product_link in enumerate(product_links, 1):
                        try:
                            logger.info(f"製品処理開始: {product_link['name']} ({product_idx}/{len(product_links)})")
                            
                            # 製品ページに移動
                            self.driver.get(product_link["url"])
                            self.utils.wait_for_page_load()
                            
                            product = {
                                "brand": "PING",
                                "model": product_link["name"],
                                "category": category["name"],
                                "type": "クラブ",
                                "url": product_link["url"],
                                "specifications": {},
                                "features": [],
                                "scraping_date": datetime.now().isoformat()
                            }
                            
                            # 仕様情報の取得
                            try:
                                spec_rows = WebDriverWait(self.driver, 10).until(
                                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.spec tr"))
                                )
                                for row in spec_rows:
                                    try:
                                        key = row.find_element(By.CSS_SELECTOR, "th").text.strip()
                                        value = row.find_element(By.CSS_SELECTOR, "td").text.strip()
                                        if key and value:
                                            product["specifications"][key] = value
                                    except Exception as e:
                                        logger.warning(f"仕様情報の取得に失敗: {str(e)}")
                                        continue
                            except Exception as e:
                                logger.warning(f"仕様テーブルの取得に失敗: {str(e)}")
                            
                            # 特徴情報の取得
                            try:
                                feature_elements = WebDriverWait(self.driver, 10).until(
                                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.feature p"))
                                )
                                product["features"] = [f.text.strip() for f in feature_elements if f.text.strip()]
                            except Exception as e:
                                logger.warning(f"特徴情報の取得に失敗: {str(e)}")
                            
                            # 価格情報の取得
                            try:
                                price_element = WebDriverWait(self.driver, 10).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, "p.price"))
                                )
                                price_text = price_element.text.strip()
                                price_match = re.search(r'¥([\d,]+)', price_text)
                                if price_match:
                                    product["price"] = int(price_match.group(1).replace(',', ''))
                                    product["is_tax_included"] = "税込" in price_text
                            except Exception as e:
                                logger.warning(f"価格情報の取得に失敗: {str(e)}")
                            
                            # 必須フィールドのチェック
                            required_fields = ["model", "category", "type"]
                            if all(product.get(field) for field in required_fields):
                                products.append(product)
                                logger.info(f"製品情報を取得: {product['model']}")
                            else:
                                logger.warning(f"必須フィールドが不足: {product}")
                            
                        except Exception as e:
                            logger.error(f"製品情報の取得に失敗: {str(e)}")
                            if self.slack:
                                self.slack.notify_error(e, {
                                    "context": "PING製品情報取得",
                                    "category": category["name"],
                                    "product": product_link["name"]
                                })
                            continue
                    
                except Exception as e:
                    logger.error(f"カテゴリーの処理に失敗: {str(e)}")
                    if self.slack:
                        self.slack.notify_error(e, {
                            "context": "PINGカテゴリー処理",
                            "category": category["name"]
                        })
                    continue
            
            logger.info(f"PING製品のスクレイピングが完了。{len(products)}件のデータを取得")
            if self.slack:
                self.slack.notify_scraping_complete("PING製品", len(products))
            
            return products
            
        except Exception as e:
            error_msg = f"PING製品のスクレイピングでエラー: {str(e)}"
            logger.error(error_msg)
            if self.slack:
                self.slack.notify_error(e, {"context": "PING製品スクレイピング"})
            raise

    def scrape_all(self) -> Dict:
        """すべてのデータをスクレイピング"""
        try:
            total_sources = 4  # スクレイピング対象の数
            results = {}
            
            # フジクラシャフト
            print("\n[1/4] フジクラシャフトのデータ収集を開始...")
            results["fujikura"] = self.scrape_fujikura()
            
            # PING製品
            print("\n[2/4] PING製品のデータ収集を開始...")
            results["ping_products"] = self.scrape_ping_products()
            
            # ゴルフダイジェスト
            print("\n[3/4] ゴルフダイジェストのデータ収集を開始...")
            results["golfdigest"] = self.scrape_golfdigest()
            
            # マサゴルフランキング
            print("\n[4/4] マサゴルフランキングのデータ収集を開始...")
            results["masa_golf_ranking"] = self.scrape_masa_golf_ranking()
            
            # 結果のサマリーを表示
            print("\nスクレイピング結果:")
            for key, value in results.items():
                print(f"- {key}: {len(value)}件のデータを取得")
            
            return results
            
        except Exception as e:
            error_msg = f"全スクレイピングに失敗: {str(e)}"
            logger.error(error_msg)
            if self.slack:
                self.slack.notify_error(e, {"context": "全スクレイピング"})
            raise

    def close(self):
        """ドライバーの終了処理"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Chromeドライバーを終了しました")
            except Exception as e:
                error_msg = f"Chromeドライバーの終了に失敗: {str(e)}"
                logger.error(error_msg)
                if self.slack:
                    self.slack.notify_error(e, {"context": "ドライバー終了"})

def save_to_database(session: Session, products: List[Dict]):
    """スクレイピング結果をデータベースに保存"""
    for product_data in products:
        try:
            # 製品情報の保存
            product = session.query(Product).filter_by(url=product_data['url']).first()
            
            if not product:
                # 新規製品の場合
                product = Product(
                    brand=product_data['brand'],
                    model=product_data['title'],
                    category=product_data['category'],
                    type=product_data.get('type', ''),
                    description=product_data['description'],
                    specifications=product_data['specifications'],
                    features=product_data['features'],
                    url=product_data['url'],
                    release_date=product_data.get('release_date')
                )
                session.add(product)
                session.flush()  # IDを取得するためにflush
            else:
                # 既存製品の場合、更新が必要な情報のみ更新
                if product_data.get('description'):
                    product.description = product_data['description']
                if product_data.get('specifications'):
                    product.specifications = product_data['specifications']
                if product_data.get('features'):
                    product.features = product_data['features']
            
            # 価格情報の保存
            if product_data.get('price'):
                # 価格から数値のみを抽出
                price_text = product_data['price']
                price_match = re.search(r'(\d{1,3}(?:,\d{3})*)', price_text)
                if price_match:
                    price = int(price_match.group(1).replace(',', ''))
                    
                    # 最新の価格を取得
                    latest_price = session.query(PriceHistory).filter_by(
                        product_id=product.id
                    ).order_by(PriceHistory.created_at.desc()).first()
                    
                    # 価格が変更されている場合のみ保存
                    if not latest_price or latest_price.price != price:
                        price_history = PriceHistory(
                            product_id=product.id,
                            price=price,
                            source=product_data['url'],
                            is_tax_included='税込' in price_text
                        )
                        session.add(price_history)
            
            session.commit()
            print(f"製品情報を保存しました: {product.brand} - {product.model}")
            
        except Exception as e:
            session.rollback()
            print(f"データベース保存でエラー: {str(e)}")
            continue

def main():
    try:
        print("スクレイピングを開始します...")
        scraper = GolfClubScraper()
        scraper.setup_driver()
        results = scraper.scrape_all()
        
        # 結果をJSONファイルに保存
        with open('golf_data.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
            
        print("\nスクレイピングが完了しました。結果を golf_data.json に保存しました。")
        
    except Exception as e:
        print(f"\nメイン処理でエラーが発生しました: {str(e)}")
        raise
    finally:
        scraper.close()

if __name__ == "__main__":
    main() 