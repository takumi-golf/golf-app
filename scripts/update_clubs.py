import json
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, JSON, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

# データベース接続設定
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデル定義
Base = declarative_base()

class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    club_id = Column(String, unique=True, index=True)
    brand = Column(String)
    model = Column(String)
    loft = Column(Float)
    shaft = Column(String)
    shaft_flex = Column(String)
    price = Column(Integer)
    features = Column(JSON)
    type = Column(String, index=True)
    specifications = Column(JSON)
    popularity_score = Column(Float, default=0.0, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    is_available = Column(Boolean, default=True, index=True)

# テーブル作成
Base.metadata.create_all(bind=engine)

def update_clubs():
    # 新しいクラブデータ
    new_clubs = [
        # ドライバー
        {"club_id": "DR001", "brand": "Titleist", "model": "TSR3", "loft": 9.0, "shaft": "TENSEI AV WHITE", "shaft_flex": "S", "price": 55000, "type": "driver", "features": {"trajectory": "低弾道", "spin": "低スピン", "forgiveness": "低"}, "specifications": {"head_volume": "460cc", "face_angle": "0.5° open"}, "is_available": True},
        {"club_id": "DR002", "brand": "Titleist", "model": "TSR2", "loft": 10.5, "shaft": "TENSEI AV BLUE", "shaft_flex": "R", "price": 55000, "type": "driver", "features": {"trajectory": "中弾道", "spin": "中スピン", "forgiveness": "中"}, "specifications": {"head_volume": "460cc", "face_angle": "0.5° closed"}, "is_available": True},
        {"club_id": "DR003", "brand": "Callaway", "model": "Paradym Triple Diamond", "loft": 9.0, "shaft": "HZRDUS BLACK", "shaft_flex": "S", "price": 58000, "type": "driver", "features": {"trajectory": "低弾道", "spin": "低スピン", "forgiveness": "低"}, "specifications": {"head_volume": "450cc", "face_angle": "1° open"}, "is_available": True},
        
        # フェアウェイウッド
        {"club_id": "FW001", "brand": "Titleist", "model": "TSR2+", "loft": 13.0, "shaft": "TENSEI AV BLUE", "shaft_flex": "R", "price": 45000, "type": "fairway", "features": {"trajectory": "中弾道", "spin": "中スピン", "forgiveness": "中"}, "specifications": {"head_volume": "175cc", "face_angle": "0.5° open"}, "is_available": True},
        {"club_id": "FW002", "brand": "Callaway", "model": "Paradym", "loft": 15.0, "shaft": "HZRDUS SILVER", "shaft_flex": "R", "price": 48000, "type": "fairway", "features": {"trajectory": "中弾道", "spin": "中スピン", "forgiveness": "中"}, "specifications": {"head_volume": "180cc", "face_angle": "0.5° closed"}, "is_available": True},
        
        # ユーティリティ
        {"club_id": "UT001", "brand": "Titleist", "model": "T200", "loft": 19.0, "shaft": "TENSEI AV WHITE", "shaft_flex": "S", "price": 40000, "type": "utility", "features": {"trajectory": "中弾道", "spin": "中スピン", "forgiveness": "中"}, "specifications": {"head_volume": "90cc", "face_angle": "0.5° open"}, "is_available": True},
        
        # アイアン
        {"club_id": "IR001", "brand": "Titleist", "model": "T100", "loft": 27.0, "shaft": "Project X", "shaft_flex": "S", "price": 180000, "type": "iron", "features": {"trajectory": "中弾道", "spin": "中スピン", "forgiveness": "低"}, "specifications": {"head_material": "鍛造", "face_technology": "精密鍛造"}, "is_available": True},
        
        # ウェッジ
        {"club_id": "WG001", "brand": "Titleist", "model": "Vokey SM9", "loft": 50.0, "shaft": "DG S200", "shaft_flex": "W", "price": 25000, "type": "wedge", "features": {"trajectory": "中弾道", "spin": "高スピン", "forgiveness": "中"}, "specifications": {"bounce": "8°", "grind": "F"}, "is_available": True},
        
        # パター
        {"club_id": "PT001", "brand": "Titleist", "model": "Scotty Cameron Special Select", "shaft": "スチール", "shaft_flex": "P", "price": 50000, "type": "putter", "features": {"alignment": "シンプル", "forgiveness": "中"}, "specifications": {"head_material": "303ステンレス", "weight": "350g"}, "is_available": True}
    ]

    db = SessionLocal()
    try:
        # 既存のデータを削除
        db.query(Club).delete()
        
        # 新しいデータを追加
        for club_data in new_clubs:
            club = Club(**club_data)
            db.add(club)
        
        db.commit()
        print("クラブデータの更新が完了しました。")
    except Exception as e:
        db.rollback()
        print(f"エラーが発生しました: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    update_clubs() 