import sqlite3
from pathlib import Path
import logging
from typing import Optional

class DatabaseConnection:
    _instance = None
    _connection = None
    _db_path = Path("database/golf_clubs.db")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        """データベース接続を取得します。"""
        if cls._connection is None:
            try:
                # データベースディレクトリの作成
                cls._db_path.parent.mkdir(parents=True, exist_ok=True)
                
                # 接続の確立
                cls._connection = sqlite3.connect(cls._db_path)
                cls._connection.row_factory = sqlite3.Row
                
                # 外部キー制約の有効化
                cls._connection.execute("PRAGMA foreign_keys = ON")
                
                logging.getLogger(__name__).info("データベース接続を確立しました。")
            except Exception as e:
                logging.getLogger(__name__).error(f"データベース接続の確立中にエラーが発生しました: {str(e)}")
                raise
        return cls._connection

    @classmethod
    def close_connection(cls) -> None:
        """データベース接続を閉じます。"""
        if cls._connection is not None:
            try:
                cls._connection.close()
                cls._connection = None
                logging.getLogger(__name__).info("データベース接続を閉じました。")
            except Exception as e:
                logging.getLogger(__name__).error(f"データベース接続のクローズ中にエラーが発生しました: {str(e)}")
                raise

    @classmethod
    def set_db_path(cls, path: Path) -> None:
        """データベースファイルのパスを設定します。"""
        if cls._connection is not None:
            raise RuntimeError("データベース接続が確立されているため、パスを変更できません。")
        cls._db_path = path

    @classmethod
    def get_db_path(cls) -> Path:
        """データベースファイルのパスを取得します。"""
        return cls._db_path

    @classmethod
    def execute_in_transaction(cls, func):
        """トランザクション内で関数を実行します。"""
        def wrapper(*args, **kwargs):
            conn = cls.get_connection()
            try:
                with conn:
                    result = func(*args, **kwargs)
                return result
            except Exception as e:
                logging.getLogger(__name__).error(f"トランザクションの実行中にエラーが発生しました: {str(e)}")
                raise
        return wrapper

def get_db():
    """データベース接続を取得する関数"""
    return DatabaseConnection().connection 