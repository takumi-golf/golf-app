import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.init_db import init_db, init_seed_data
from app.database import SessionLocal

def main():
    print("データベースを初期化しています...")
    init_db()
    
    print("シードデータを投入しています...")
    db = SessionLocal()
    try:
        init_seed_data(db)
        print("シードデータの投入が完了しました。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main() 