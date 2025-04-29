from typing import Dict, List, Any
import os
from dotenv import load_dotenv

load_dotenv()

class ScraperConfig:
    """スクレイピングの設定クラス"""
    
    # ベースURL
    BASE_URL = "https://golfnavi.info"
    
    # カテゴリID
    CATEGORY_IDS = {
        "driver": 21,  # ドライバー
        "fairway_wood": 22,  # フェアウェイウッド
        "utility": 23,  # ユーティリティ
        "iron": 24,  # アイアン
        "wedge": 25,  # ウェッジ
        "putter": 26,  # パター
        "club_set": 27  # クラブセット
    }
    
    # メーカー一覧
    MANUFACTURERS = [
        "テーラーメイド", "キャロウェイ", "ミズノ", "タイトリスト", "ピン",
        "ブリヂストン", "ダンロップ", "フォーティーン", "クリーブランド",
        "コブラ", "ナイキ", "ウィルソン", "ヤマハ", "本間ゴルフ"
    ]
    
    # スクレイピング間隔（秒）
    SCRAPING_INTERVAL = 1
    
    # リトライ設定
    MAX_RETRIES = 3
    RETRY_DELAY = 5
    
    # データ保存先
    DATA_DIR = "data"
    RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
    
    # データファイル名
    DATA_FILES = {
        "driver": "drivers.json",
        "fairway_wood": "fairway_woods.json",
        "utility": "utilities.json",
        "iron": "irons.json",
        "wedge": "wedges.json",
        "putter": "putters.json",
        "club_set": "club_sets.json"
    }
    
    # スクレイピング対象のフィールド
    TARGET_FIELDS = {
        "basic": [
            "name",  # クラブ名
            "manufacturer",  # メーカー
            "category",  # カテゴリ
            "release_year",  # 発売年
            "price",  # 価格
        ],
        "specs": [
            "loft",  # ロフト角
            "lie",  # ライ角
            "face_angle",  # フェース角
            "length",  # 長さ
            "shaft",  # シャフト
            "flex",  # フレックス
            "weight",  # 重量
        ],
        "features": [
            "forgiveness",  # 許容性
            "distance",  # 飛距離
            "control",  # コントロール性
            "feel",  # 打感
            "look",  # 見た目
        ]
    }
    
    # スクレイピングのスケジュール
    SCHEDULE = {
        "daily": True,  # 毎日実行
        "time": "03:00",  # 実行時間
        "timezone": "Asia/Tokyo"  # タイムゾーン
    } 