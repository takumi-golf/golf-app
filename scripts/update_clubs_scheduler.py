import schedule
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from typing import Dict, List, Optional
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('club_updates.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Slack設定
SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_CHANNEL = "#golf-club-updates"
slack_client = WebClient(token=SLACK_TOKEN) if SLACK_TOKEN else None

def send_slack_notification(message: str, attachments: Optional[List[Dict]] = None):
    """
    Slackに通知を送信
    """
    if not slack_client:
        logger.warning("Slack tokenが設定されていないため、通知はスキップされます")
        return

    try:
        slack_client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=message,
            attachments=attachments
        )
    except SlackApiError as e:
        logger.error(f"Slack通知エラー: {str(e)}")

class GolfShopScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def fetch_from_golf_partner(self) -> List[Dict]:
        """
        ゴルフパートナーからデータを取得
        """
        clubs_data = []
        base_urls = {
            "driver": "https://www.golfpartner.co.jp/club/driver/",
            "fairway": "https://www.golfpartner.co.jp/club/fw/",
            "utility": "https://www.golfpartner.co.jp/club/ut/",
            "iron": "https://www.golfpartner.co.jp/club/iron/",
            "wedge": "https://www.golfpartner.co.jp/club/wedge/",
            "putter": "https://www.golfpartner.co.jp/club/putter/"
        }

        for club_type, url in base_urls.items():
            try:
                response = requests.get(url, headers=self.headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 実際のサイト構造に合わせて調整が必要
                for item in soup.find_all("div", class_="club-item"):
                    club_data = self._parse_golf_partner_item(item, club_type)
                    if club_data:
                        clubs_data.append(club_data)
                
                time.sleep(2)  # サイトへの負荷軽減
            except Exception as e:
                logger.error(f"ゴルフパートナーのスクレイピングエラー: {str(e)}")

        return clubs_data

    def fetch_from_victoria(self) -> List[Dict]:
        """
        ヴィクトリアゴルフからデータを取得
        """
        clubs_data = []
        base_urls = {
            "driver": "https://www.victoria.co.jp/golf/club/driver",
            "fairway": "https://www.victoria.co.jp/golf/club/fairway",
            # 他のクラブタイプのURLを追加
        }

        for club_type, url in base_urls.items():
            try:
                response = requests.get(url, headers=self.headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 実際のサイト構造に合わせて調整が必要
                for item in soup.find_all("div", class_="item"):
                    club_data = self._parse_victoria_item(item, club_type)
                    if club_data:
                        clubs_data.append(club_data)
                
                time.sleep(2)
            except Exception as e:
                logger.error(f"ヴィクトリアゴルフのスクレイピングエラー: {str(e)}")

        return clubs_data

    def _parse_golf_partner_item(self, item, club_type: str) -> Optional[Dict]:
        """
        ゴルフパートナーの商品情報をパース
        """
        try:
            specs = item.find("div", class_="specs")
            return {
                "shop": "GolfPartner",
                "brand": item.find("div", class_="brand").text.strip(),
                "model": item.find("div", class_="model").text.strip(),
                "price": int(item.find("div", class_="price").text.strip().replace("¥", "").replace(",", "")),
                "type": club_type,
                "specs": {
                    "loft": specs.find("div", class_="loft").text.strip() if specs else None,
                    "shaft": specs.find("div", class_="shaft").text.strip() if specs else None,
                    "flex": specs.find("div", class_="flex").text.strip() if specs else None
                },
                "url": item.find("a")["href"],
                "updated_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"ゴルフパートナーの商品パースエラー: {str(e)}")
            return None

    def _parse_victoria_item(self, item, club_type: str) -> Optional[Dict]:
        """
        ヴィクトリアゴルフの商品情報をパース
        """
        try:
            specs = item.find("div", class_="specs")
            return {
                "shop": "Victoria",
                "brand": item.find("div", class_="brand").text.strip(),
                "model": item.find("div", class_="model").text.strip(),
                "price": int(item.find("div", class_="price").text.strip().replace("¥", "").replace(",", "")),
                "type": club_type,
                "specs": {
                    "loft": specs.find("div", class_="loft").text.strip() if specs else None,
                    "shaft": specs.find("div", class_="shaft").text.strip() if specs else None,
                    "flex": specs.find("div", class_="flex").text.strip() if specs else None
                },
                "url": item.find("a")["href"],
                "updated_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"ヴィクトリアゴルフの商品パースエラー: {str(e)}")
            return None

class ClubDatabase:
    def __init__(self):
        DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
        self.engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def update_clubs(self, clubs_data: List[Dict]):
        """
        クラブデータをデータベースに更新
        """
        if not clubs_data:
            return

        db = self.SessionLocal()
        try:
            for club in clubs_data:
                # 既存のデータを検索
                existing = db.execute(
                    text("SELECT * FROM clubs WHERE brand = :brand AND model = :model AND shop = :shop"),
                    {"brand": club["brand"], "model": club["model"], "shop": club["shop"]}
                ).fetchone()

                if existing:
                    # 価格変動を記録
                    if existing.price != club["price"]:
                        self._record_price_change(db, existing, club)
                    
                    # データを更新
                    db.execute(
                        text("""
                        UPDATE clubs 
                        SET price = :price, specs = :specs, updated_at = :updated_at
                        WHERE brand = :brand AND model = :model AND shop = :shop
                        """),
                        {
                            "price": club["price"],
                            "specs": json.dumps(club["specs"]),
                            "updated_at": club["updated_at"],
                            "brand": club["brand"],
                            "model": club["model"],
                            "shop": club["shop"]
                        }
                    )
                else:
                    # 新規データを追加
                    db.execute(
                        text("""
                        INSERT INTO clubs (
                            shop, brand, model, price, type, specs, url, updated_at
                        ) VALUES (
                            :shop, :brand, :model, :price, :type, :specs, :url, :updated_at
                        )
                        """),
                        {
                            **club,
                            "specs": json.dumps(club["specs"])
                        }
                    )

            db.commit()
            logger.info("クラブデータの更新が完了しました")
            
        except Exception as e:
            db.rollback()
            logger.error(f"データベース更新エラー: {str(e)}")
        finally:
            db.close()

    def _record_price_change(self, db, existing, new_data):
        """
        価格変動を記録
        """
        try:
            db.execute(
                text("""
                INSERT INTO price_history (
                    club_id, old_price, new_price, changed_at
                ) VALUES (
                    :club_id, :old_price, :new_price, :changed_at
                )
                """),
                {
                    "club_id": existing.id,
                    "old_price": existing.price,
                    "new_price": new_data["price"],
                    "changed_at": datetime.now().isoformat()
                }
            )

            # 価格変動をSlackに通知
            price_diff = new_data["price"] - existing.price
            diff_text = "値上げ" if price_diff > 0 else "値下げ"
            message = f"価格変動検知: {new_data['brand']} {new_data['model']}\n"
            message += f"{abs(price_diff):,}円の{diff_text}（{existing.price:,}円 → {new_data['price']:,}円）"
            
            send_slack_notification(message, [{
                "color": "#36a64f" if price_diff < 0 else "#ff0000",
                "title": f"{new_data['shop']}の価格変動",
                "text": message,
                "fields": [
                    {
                        "title": "商品URL",
                        "value": new_data["url"],
                        "short": False
                    }
                ]
            }])

        except Exception as e:
            logger.error(f"価格履歴の記録エラー: {str(e)}")

def job():
    """
    定期実行するジョブ
    """
    logger.info("クラブ情報の更新を開始します")
    
    scraper = GolfShopScraper()
    db = ClubDatabase()
    
    # 各ショップからデータを取得
    clubs_data = []
    clubs_data.extend(scraper.fetch_from_golf_partner())
    clubs_data.extend(scraper.fetch_from_victoria())
    
    if clubs_data:
        # データベースを更新
        db.update_clubs(clubs_data)
        
        # 更新サマリーをSlackに通知
        summary = f"クラブ情報の更新が完了しました\n"
        summary += f"- 取得件数: {len(clubs_data)}件\n"
        summary += f"- 更新時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        send_slack_notification(summary)
    else:
        error_msg = "クラブ情報の取得に失敗しました"
        logger.error(error_msg)
        send_slack_notification(f"⚠️ {error_msg}")

def main():
    # 毎日午前3時に実行
    schedule.every().day.at("03:00").do(job)
    
    # 起動時に1回実行
    job()
    
    # スケジューラーの実行
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main() 