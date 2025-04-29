import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# データベース接続情報
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

# 自動コミットモードに設定
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

try:
    # カーソルを作成
    cur = conn.cursor()
    
    # データベースが存在するか確認
    cur.execute("SELECT 1 FROM pg_database WHERE datname = 'golf_db'")
    exists = cur.fetchone()
    
    if not exists:
        # データベースを作成
        cur.execute("CREATE DATABASE golf_db")
        print("データベース 'golf_db' を作成しました")
    else:
        print("データベース 'golf_db' は既に存在します")
    
    # カーソルを閉じる
    cur.close()

except Exception as e:
    print(f"エラーが発生しました: {e}")

finally:
    # 接続を閉じる
    conn.close() 