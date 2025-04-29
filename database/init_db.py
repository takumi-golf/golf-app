import logging
from pathlib import Path
from db_manager import DatabaseManager
from db_connection import DatabaseConnection

def setup_logging():
    """ロギングの設定を行います。"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('database/init.log'),
            logging.StreamHandler()
        ]
    )

def main():
    """データベースの初期化とマイグレーションを実行します。"""
    # ロギングの設定
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # データベースマネージャーの初期化
        db_manager = DatabaseManager()
        
        # データベースの初期化
        logger.info("データベースの初期化を開始します...")
        if db_manager.initialize_database():
            logger.info("データベースの初期化が完了しました。")
        else:
            logger.error("データベースの初期化に失敗しました。")
            return
            
        # マイグレーションの適用
        logger.info("マイグレーションの適用を開始します...")
        db_manager.apply_migrations()
        logger.info("マイグレーションの適用が完了しました。")
        
        # バックアップの作成
        backup_path = Path("database/backups/initial_backup.db")
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info("初期バックアップの作成を開始します...")
        if db_manager.backup_database(backup_path):
            logger.info(f"初期バックアップが作成されました: {backup_path}")
        else:
            logger.error("初期バックアップの作成に失敗しました。")
            
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        raise
    finally:
        # データベース接続のクローズ
        DatabaseConnection.close_connection()
        logger.info("データベース接続を閉じました。")

if __name__ == "__main__":
    main() 