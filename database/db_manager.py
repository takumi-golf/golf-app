import os
import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging
from .db_connection import DatabaseConnection

class DatabaseManager:
    def __init__(self):
        self.db_path = Path("database/golf_clubs.db")
        self.schema_path = Path("database/schema.sql")
        self.migrations_path = Path("database/migrations")
        self.logger = logging.getLogger(__name__)
        
    def initialize_database(self) -> bool:
        """データベースを初期化します。"""
        try:
            # データベースディレクトリが存在しない場合は作成
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            
            # スキーマファイルが存在する場合は実行
            if self.schema_path.exists():
                with open(self.schema_path, "r", encoding="utf-8") as f:
                    schema_sql = f.read()
                
                conn = DatabaseConnection.get_connection()
                cursor = conn.cursor()
                cursor.executescript(schema_sql)
                conn.commit()
                
                self.logger.info("データベースの初期化が完了しました。")
                return True
            else:
                self.logger.error("スキーマファイルが見つかりません。")
                return False
                
        except Exception as e:
            self.logger.error(f"データベースの初期化中にエラーが発生しました: {str(e)}")
            return False
            
    def apply_migrations(self) -> None:
        """未適用のマイグレーションを実行します。"""
        try:
            if not self.migrations_path.exists():
                self.logger.info("マイグレーションディレクトリが存在しません。")
                return
                
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            
            # マイグレーション履歴テーブルが存在しない場合は作成
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS migration_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    migration_name TEXT NOT NULL UNIQUE,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 既に適用済みのマイグレーションを取得
            cursor.execute("SELECT migration_name FROM migration_history")
            applied_migrations = {row[0] for row in cursor.fetchall()}
            
            # マイグレーションファイルを取得してソート
            migration_files = sorted(
                [f for f in self.migrations_path.glob("*.sql")],
                key=lambda x: x.name
            )
            
            # 未適用のマイグレーションを実行
            for migration_file in migration_files:
                if migration_file.name not in applied_migrations:
                    with open(migration_file, "r", encoding="utf-8") as f:
                        migration_sql = f.read()
                    
                    cursor.executescript(migration_sql)
                    cursor.execute(
                        "INSERT INTO migration_history (migration_name) VALUES (?)",
                        (migration_file.name,)
                    )
                    conn.commit()
                    self.logger.info(f"マイグレーション {migration_file.name} を適用しました。")
                    
        except Exception as e:
            self.logger.error(f"マイグレーションの適用中にエラーが発生しました: {str(e)}")
            raise
            
    def backup_database(self, backup_path: Path) -> bool:
        """データベースのバックアップを作成します。"""
        try:
            conn = DatabaseConnection.get_connection()
            backup_conn = sqlite3.connect(backup_path)
            
            # バックアップの作成
            conn.backup(backup_conn)
            backup_conn.close()
            
            self.logger.info(f"データベースのバックアップが完了しました: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"データベースのバックアップ中にエラーが発生しました: {str(e)}")
            return False
            
    def restore_database(self, backup_path: Path) -> bool:
        """バックアップからデータベースを復元します。"""
        try:
            # 現在のデータベースを閉じる
            DatabaseConnection.close_connection()

            # バックアップファイルの存在確認
            if not backup_path.exists():
                raise FileNotFoundError(f"バックアップファイルが見つかりません: {backup_path}")
                
            # 現在のデータベースを削除
            if self.db_path.exists():
                self.db_path.unlink()

            # バックアップから復元
            backup_conn = sqlite3.connect(backup_path)
            conn = sqlite3.connect(self.db_path)
            backup_conn.backup(conn)
            backup_conn.close()
            conn.close()
            
            self.logger.info(f"データベースの復元が完了しました: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"データベースの復元中にエラーが発生しました: {str(e)}")
            return False

    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """SQLクエリを実行し、結果を返します。"""
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # 結果の取得
            columns = [description[0] for description in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))

            return results

        except Exception as e:
            self.logger.error(f"クエリの実行中にエラーが発生しました: {str(e)}")
            raise

    def execute_many(self, query: str, params_list: List[tuple]) -> None:
        """複数のパラメータで同じクエリを実行します。"""
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()

            cursor.executemany(query, params_list)
            conn.commit()

        except Exception as e:
            self.logger.error(f"一括クエリの実行中にエラーが発生しました: {str(e)}")
            raise

    def insert_data(self, table: str, data: Dict[str, Any]) -> int:
        """データをテーブルに挿入し、挿入されたレコードのIDを返します。"""
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()

            # カラム名と値を分離
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["?"] * len(data))
            values = tuple(data.values())

            # クエリの構築と実行
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, values)
            conn.commit()

            return cursor.lastrowid

        except Exception as e:
            self.logger.error(f"データの挿入中にエラーが発生しました: {str(e)}")
            raise

    def update_data(self, table: str, data: Dict[str, Any], where: str, where_params: tuple) -> int:
        """テーブルのデータを更新し、更新された行数を返します。"""
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()

            # 更新するカラムと値を構築
            set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
            values = tuple(data.values()) + where_params

            # クエリの構築と実行
            query = f"UPDATE {table} SET {set_clause} WHERE {where}"
            cursor.execute(query, values)
            conn.commit()

            return cursor.rowcount

        except Exception as e:
            self.logger.error(f"データの更新中にエラーが発生しました: {str(e)}")
            raise

    def delete_data(self, table: str, where: str, where_params: tuple) -> int:
        """テーブルからデータを削除し、削除された行数を返します。"""
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()

            # クエリの構築と実行
            query = f"DELETE FROM {table} WHERE {where}"
            cursor.execute(query, where_params)
            conn.commit()

            return cursor.rowcount

        except Exception as e:
            self.logger.error(f"データの削除中にエラーが発生しました: {str(e)}")
            raise 