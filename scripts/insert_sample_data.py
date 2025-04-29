from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
from pathlib import Path
from datetime import datetime
import json

# プロジェクトのルートディレクトリをPythonパスに追加
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from scripts.models import Club

# データベース接続設定
DATABASE_URL = "sqlite:///./golf_clubs.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def insert_sample_data():
    db = SessionLocal()

    try:
        # サンプルデータの作成
        sample_clubs = [
            Club(
                club_id="TSI3-001",
                brand="Titleist",
                model="TSi3",
                type="driver",
                loft=9.5,
                shaft="Diamana",
                shaft_flex="S",
                price=50000,
                features=json.dumps({
                    "description": "低スピン設計で安定した飛距離を実現",
                    "trajectory": "中弾道",
                    "spin": "低スピン",
                    "forgiveness": "中"
                }),
                specifications=json.dumps({
                    "head_volume": "460cc",
                    "length": "45.5インチ",
                    "weight": "320g"
                })
            ),
            Club(
                club_id="EPIC-001",
                brand="Callaway",
                model="Epic Max",
                type="driver",
                loft=10.5,
                shaft="Project X",
                shaft_flex="R",
                price=48000,
                features=json.dumps({
                    "description": "AI設計による最適化されたヘッド形状",
                    "trajectory": "高弾道",
                    "spin": "中スピン",
                    "forgiveness": "高"
                }),
                specifications=json.dumps({
                    "head_volume": "460cc",
                    "length": "45.75インチ",
                    "weight": "315g"
                })
            )
        ]

        # データの挿入
        for club in sample_clubs:
            db.add(club)
        
        db.commit()
        print("サンプルデータの挿入が完了しました。")

    except Exception as e:
        db.rollback()
        print(f"エラーが発生しました: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    insert_sample_data() 