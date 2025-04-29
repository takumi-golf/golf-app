import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# プロジェクトのルートディレクトリをPythonパスに追加
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# データベース接続設定
DATABASE_URL = "sqlite:///./golf_clubs.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# セッションの作成
db = SessionLocal()

try:
    # Clubテーブルの内容を表示
    clubs = db.execute(text("SELECT * FROM clubs")).fetchall()
    print(f"クラブの総数: {len(clubs)}")
    print("\n最初の5件のクラブデータ:")
    for club in clubs[:5]:
        print(f"ブランド: {club.brand}, モデル: {club.model}, ロフト: {club.loft}, 価格: {club.price}円")
finally:
    db.close() 