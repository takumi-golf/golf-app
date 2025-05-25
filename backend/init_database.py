import sys
from pathlib import Path
import importlib
import os

# プロジェクトのルートディレクトリをPythonパスに追加
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def clean_database():
    """データベースファイルを完全に削除"""
    db_file = Path(project_root) / "golf_recommendation.db"
    if db_file.exists():
        try:
            os.remove(db_file)
            print("既存のデータベースファイルを削除しました。")
        except Exception as e:
            print(f"データベースファイルの削除中にエラーが発生しました: {e}")

# 必要なモジュールを再読み込み
def reload_modules():
    """全ての関連モジュールを再読み込み"""
    modules_to_reload = [
        'app.models.club',
        'app.models.recommendation',
        'app.database',
        'app.db.init_db'
    ]
    
    for module_name in modules_to_reload:
        try:
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])
                print(f"モジュール {module_name} を再読み込みしました。")
        except Exception as e:
            print(f"モジュール {module_name} の再読み込み中にエラーが発生しました: {e}")

# 必要なコンポーネントをインポート
from app.models import Base
from app.db.init_db import init_db, init_seed_data
from app.database import SessionLocal

def main():
    print("データベースの初期化を開始します...")
    
    # データベースをクリーンアップ
    clean_database()
    
    # モジュールを再読み込み
    reload_modules()
    
    print("データベーススキーマを作成しています...")
    init_db()
    
    print("シードデータを挿入しています...")
    db = SessionLocal()
    try:
        init_seed_data(db)
        print("データベースの初期化が完了しました。")
    except Exception as e:
        print(f"シードデータの挿入中にエラーが発生しました: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main() 