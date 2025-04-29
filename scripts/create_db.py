from sqlalchemy import create_engine
from app.database import Base

# データベース接続設定
engine = create_engine('sqlite:///./test.db')

# テーブル作成
Base.metadata.create_all(bind=engine)
print("データベースとテーブルが作成されました。") 