from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, Club
import os

# データベース接続設定
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# クラブデータ
clubs_data = [
    # ドライバー
    {
        "brand": "Titleist",
        "model": "TSi3",
        "loft": 9.5,
        "shaft": "Diamana",
        "shaft_flex": "S",
        "price": 50000,
        "features": "低スピン、高弾道",
        "type": "driver"
    },
    {
        "brand": "Callaway",
        "model": "Paradym",
        "loft": 10.5,
        "shaft": "Project X",
        "shaft_flex": "S",
        "price": 48000,
        "features": "高弾道、高容錯性",
        "type": "driver"
    },
    {
        "brand": "TaylorMade",
        "model": "Stealth 2",
        "loft": 9.0,
        "shaft": "Fujikura",
        "shaft_flex": "S",
        "price": 52000,
        "features": "低スピン、高弾道",
        "type": "driver"
    },
    # フェアウェイウッド
    {
        "brand": "Titleist",
        "model": "TSi2",
        "loft": 15,
        "shaft": "Diamana",
        "shaft_flex": "S",
        "price": 40000,
        "features": "高弾道、高容錯性",
        "type": "wood"
    },
    {
        "brand": "Callaway",
        "model": "Paradym",
        "loft": 15,
        "shaft": "Project X",
        "shaft_flex": "S",
        "price": 38000,
        "features": "高弾道、高容錯性",
        "type": "wood"
    },
    # ユーティリティ
    {
        "brand": "Titleist",
        "model": "U505",
        "loft": 21,
        "shaft": "Diamana",
        "shaft_flex": "S",
        "price": 35000,
        "features": "アイアンライクな操作性",
        "type": "utility"
    },
    {
        "brand": "Callaway",
        "model": "Apex UW",
        "loft": 21,
        "shaft": "Project X",
        "shaft_flex": "S",
        "price": 33000,
        "features": "高弾道、高容錯性",
        "type": "utility"
    },
    # アイアン
    {
        "brand": "Titleist",
        "model": "T200",
        "loft": 27,
        "shaft": "Dynamic Gold",
        "shaft_flex": "S",
        "price": 30000,
        "features": "高弾道、高容錯性",
        "type": "iron"
    },
    {
        "brand": "Callaway",
        "model": "Apex",
        "loft": 27,
        "shaft": "Project X",
        "shaft_flex": "S",
        "price": 28000,
        "features": "高弾道、高容錯性",
        "type": "iron"
    },
    # ウェッジ
    {
        "brand": "Titleist",
        "model": "Vokey SM9",
        "loft": 52,
        "shaft": "Dynamic Gold",
        "shaft_flex": "S",
        "price": 25000,
        "features": "スピン性能抜群",
        "type": "wedge"
    },
    {
        "brand": "Callaway",
        "model": "Jaws",
        "loft": 52,
        "shaft": "Project X",
        "shaft_flex": "S",
        "price": 23000,
        "features": "スピン性能抜群",
        "type": "wedge"
    },
    # パター
    {
        "brand": "Scotty Cameron",
        "model": "Special Select",
        "loft": 3,
        "shaft": "Steel",
        "shaft_flex": "Standard",
        "price": 45000,
        "features": "安定したストローク",
        "type": "putter"
    },
    {
        "brand": "Odyssey",
        "model": "White Hot OG",
        "loft": 3,
        "shaft": "Steel",
        "shaft_flex": "Standard",
        "price": 43000,
        "features": "安定したストローク",
        "type": "putter"
    }
]

def seed_clubs():
    db = SessionLocal()
    try:
        # 既存のデータを削除
        db.query(Club).delete()
        
        # 新しいデータを追加
        for club_data in clubs_data:
            club = Club(**club_data)
            db.add(club)
        
        db.commit()
        print("クラブデータのシードが完了しました。")
    except Exception as e:
        db.rollback()
        print(f"エラーが発生しました: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_clubs() 