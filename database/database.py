import sqlite3
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple, Union
import os
import json

# ロギングの設定
logging.basicConfig(
    filename='logs/database_access.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Database:
    def __init__(self, db_path: str = 'database/golf_clubs.db'):
        """データベース接続を初期化します。
        
        Args:
            db_path (str): データベースファイルのパス
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self) -> None:
        """データベースに接続します。"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            logging.info(f"データベースに接続しました: {self.db_path}")
        except sqlite3.Error as e:
            logging.error(f"データベース接続エラー: {e}")
            raise

    def close(self) -> None:
        """データベース接続を閉じます。"""
        if self.conn:
            self.conn.close()
            logging.info("データベース接続を閉じました")

    def execute(self, query: str, params: Tuple = None) -> None:
        """SQLクエリを実行します。
        
        Args:
            query (str): 実行するSQLクエリ
            params (Tuple, optional): クエリのパラメータ
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            logging.info(f"クエリを実行しました: {query}")
        except sqlite3.Error as e:
            self.conn.rollback()
            logging.error(f"クエリ実行エラー: {e}, クエリ: {query}")
            raise

    def fetch_one(self, query: str, params: Tuple = None) -> Optional[Dict[str, Any]]:
        """1行の結果を取得します。
        
        Args:
            query (str): 実行するSQLクエリ
            params (Tuple, optional): クエリのパラメータ
            
        Returns:
            Optional[Dict[str, Any]]: 結果の行、存在しない場合はNone
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            logging.error(f"データ取得エラー: {e}, クエリ: {query}")
            raise

    def fetch_all(self, query: str, params: Tuple = None) -> List[Dict[str, Any]]:
        """すべての結果を取得します。
        
        Args:
            query (str): 実行するSQLクエリ
            params (Tuple, optional): クエリのパラメータ
            
        Returns:
            List[Dict[str, Any]]: 結果の行のリスト
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            logging.error(f"データ取得エラー: {e}, クエリ: {query}")
            raise

    def initialize_database(self) -> None:
        """データベースを初期化し、テーブルを作成します。"""
        try:
            with open('database/schema.sql', 'r', encoding='utf-8') as f:
                schema = f.read()
            self.cursor.executescript(schema)
            self.conn.commit()
            logging.info("データベースを初期化しました")
        except (sqlite3.Error, IOError) as e:
            self.conn.rollback()
            logging.error(f"データベース初期化エラー: {e}")
            raise

    def backup_database(self, backup_path: str = None) -> None:
        """データベースのバックアップを作成します。
        
        Args:
            backup_path (str, optional): バックアップファイルのパス
        """
        if backup_path is None:
            backup_path = f"backups/golf_clubs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        
        try:
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            with sqlite3.connect(backup_path) as backup_conn:
                self.conn.backup(backup_conn)
            logging.info(f"データベースのバックアップを作成しました: {backup_path}")
        except (sqlite3.Error, IOError) as e:
            logging.error(f"バックアップ作成エラー: {e}")
            raise

    def __enter__(self):
        """コンテキストマネージャーのエントリーポイント"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """コンテキストマネージャーのエグジットポイント"""
        self.close()

class GolfClubDatabase(Database):
    """ゴルフクラブデータベース操作クラス"""
    
    def add_manufacturer(self, data: Dict[str, Any]) -> int:
        """メーカー情報を追加します。
        
        Args:
            data (Dict[str, Any]): メーカー情報
            
        Returns:
            int: 追加されたメーカーのID
        """
        query = """
        INSERT INTO manufacturers (name, country, website, established_year, notes)
        VALUES (?, ?, ?, ?, ?)
        """
        params = (
            data['name'],
            data.get('country'),
            data.get('website'),
            data.get('established_year'),
            data.get('notes')
        )
        self.execute(query, params)
        return self.cursor.lastrowid

    def add_club_series(self, data: Dict[str, Any]) -> int:
        """クラブシリーズ情報を追加します。
        
        Args:
            data (Dict[str, Any]): シリーズ情報
            
        Returns:
            int: 追加されたシリーズのID
        """
        query = """
        INSERT INTO series (manufacturer_id, name, release_year, target_handicap_range,
                          technology_description, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            data['manufacturer_id'],
            data['name'],
            data.get('release_year'),
            data.get('target_handicap_range'),
            data.get('technology_description'),
            data.get('notes')
        )
        self.execute(query, params)
        return self.cursor.lastrowid

    def add_club_model(self, data: Dict[str, Any]) -> int:
        """クラブモデル情報を追加します。
        
        Args:
            data (Dict[str, Any]): モデル情報
            
        Returns:
            int: 追加されたモデルのID
        """
        query = """
        INSERT INTO models (series_id, name, club_type, loft_range, length_range,
                          weight_range, stock_options, msrp, release_year, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            data['series_id'],
            data['name'],
            data['club_type'],
            json.dumps(data.get('loft_range', [])),
            json.dumps(data.get('length_range', [])),
            json.dumps(data.get('weight_range', [])),
            json.dumps(data.get('stock_options', {})),
            data.get('msrp'),
            data.get('release_year'),
            data.get('notes')
        )
        self.execute(query, params)
        return self.cursor.lastrowid

    def add_performance_data(self, data: Dict[str, Any]) -> int:
        """性能データを追加します。
        
        Args:
            data (Dict[str, Any]): 性能データ
            
        Returns:
            int: 追加された性能データのID
        """
        query = """
        INSERT INTO performance_data (model_id, carry_distance, total_distance,
                                    launch_angle, spin_rate, ball_speed, club_speed,
                                    smash_factor, dispersion, peak_height,
                                    descent_angle, date, conditions, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            data['model_id'],
            data.get('carry_distance'),
            data.get('total_distance'),
            data.get('launch_angle'),
            data.get('spin_rate'),
            data.get('ball_speed'),
            data.get('club_speed'),
            data.get('smash_factor'),
            data.get('dispersion'),
            data.get('peak_height'),
            data.get('descent_angle'),
            data.get('date'),
            json.dumps(data.get('conditions', {})),
            data.get('notes')
        )
        self.execute(query, params)
        return self.cursor.lastrowid

    def get_manufacturer(self, name: str) -> Optional[Dict[str, Any]]:
        """メーカー情報を取得します。
        
        Args:
            name (str): メーカー名
            
        Returns:
            Optional[Dict[str, Any]]: メーカー情報
        """
        query = "SELECT * FROM manufacturers WHERE name = ?"
        return self.fetch_one(query, (name,))

    def get_series(self, manufacturer_id: int, name: str) -> Optional[Dict[str, Any]]:
        """シリーズ情報を取得します。
        
        Args:
            manufacturer_id (int): メーカーID
            name (str): シリーズ名
            
        Returns:
            Optional[Dict[str, Any]]: シリーズ情報
        """
        query = "SELECT * FROM series WHERE manufacturer_id = ? AND name = ?"
        return self.fetch_one(query, (manufacturer_id, name))

    def get_model(self, series_id: int, name: str) -> Optional[Dict[str, Any]]:
        """モデル情報を取得します。
        
        Args:
            series_id (int): シリーズID
            name (str): モデル名
            
        Returns:
            Optional[Dict[str, Any]]: モデル情報
        """
        query = "SELECT * FROM models WHERE series_id = ? AND name = ?"
        return self.fetch_one(query, (series_id, name))

    def get_performance_data(self, model_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """性能データを取得します。
        
        Args:
            model_id (int): モデルID
            limit (int): 取得件数
            
        Returns:
            List[Dict[str, Any]]: 性能データのリスト
        """
        query = """
        SELECT * FROM performance_data
        WHERE model_id = ?
        ORDER BY date DESC
        LIMIT ?
        """
        return self.fetch_all(query, (model_id, limit))

    def update_manufacturer(self, manufacturer_id: int, data: Dict[str, Any]) -> None:
        """メーカー情報を更新します。
        
        Args:
            manufacturer_id (int): メーカーID
            data (Dict[str, Any]): 更新するデータ
        """
        query = """
        UPDATE manufacturers
        SET name = ?, country = ?, website = ?, established_year = ?, notes = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """
        params = (
            data.get('name'),
            data.get('country'),
            data.get('website'),
            data.get('established_year'),
            data.get('notes'),
            manufacturer_id
        )
        self.execute(query, params)

    def update_series(self, series_id: int, data: Dict[str, Any]) -> None:
        """シリーズ情報を更新します。
        
        Args:
            series_id (int): シリーズID
            data (Dict[str, Any]): 更新するデータ
        """
        query = """
        UPDATE series
        SET name = ?, release_year = ?, target_handicap_range = ?,
            technology_description = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """
        params = (
            data.get('name'),
            data.get('release_year'),
            data.get('target_handicap_range'),
            data.get('technology_description'),
            data.get('notes'),
            series_id
        )
        self.execute(query, params)

    def update_model(self, model_id: int, data: Dict[str, Any]) -> None:
        """モデル情報を更新します。
        
        Args:
            model_id (int): モデルID
            data (Dict[str, Any]): 更新するデータ
        """
        query = """
        UPDATE models
        SET name = ?, club_type = ?, loft_range = ?, length_range = ?,
            weight_range = ?, stock_options = ?, msrp = ?, release_year = ?,
            notes = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """
        params = (
            data.get('name'),
            data.get('club_type'),
            json.dumps(data.get('loft_range', [])),
            json.dumps(data.get('length_range', [])),
            json.dumps(data.get('weight_range', [])),
            json.dumps(data.get('stock_options', {})),
            data.get('msrp'),
            data.get('release_year'),
            data.get('notes'),
            model_id
        )
        self.execute(query, params)

    def delete_manufacturer(self, manufacturer_id: int) -> None:
        """メーカー情報を削除します。
        
        Args:
            manufacturer_id (int): メーカーID
        """
        query = "DELETE FROM manufacturers WHERE id = ?"
        self.execute(query, (manufacturer_id,))

    def delete_series(self, series_id: int) -> None:
        """シリーズ情報を削除します。
        
        Args:
            series_id (int): シリーズID
        """
        query = "DELETE FROM series WHERE id = ?"
        self.execute(query, (series_id,))

    def delete_model(self, model_id: int) -> None:
        """モデル情報を削除します。
        
        Args:
            model_id (int): モデルID
        """
        query = "DELETE FROM models WHERE id = ?"
        self.execute(query, (model_id,))

    def delete_performance_data(self, performance_id: int) -> None:
        """性能データを削除します。
        
        Args:
            performance_id (int): 性能データID
        """
        query = "DELETE FROM performance_data WHERE id = ?"
        self.execute(query, (performance_id,))

# 使用例
if __name__ == "__main__":
    # データベースの初期化
    with GolfClubDatabase() as db:
        db.initialize_database()
        db.backup_database() 