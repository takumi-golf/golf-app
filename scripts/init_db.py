import os
import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# プロジェクトのルートディレクトリをPythonパスに追加
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# データベースのベースクラスを作成
Base = declarative_base()

# データベース接続設定
DATABASE_URL = "sqlite:///./golf_clubs.db"

def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("データベースの初期化が完了しました。")

if __name__ == "__main__":
    init_db() 