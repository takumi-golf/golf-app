import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import logging
from typing import Dict, List, Optional, Union
import time
import random
from pathlib import Path
from database.database import GolfClubDatabase

class GolfClubDataCollector:
    """ゴルフクラブデータ収集クラス"""
    
    def __init__(self, db_path: Union[str, Path] = "golf_clubs.db"):
        self.db = GolfClubDatabase(db_path)
        self._setup_logging()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def _setup_logging(self):
        """ロギングの設定"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('data_collection.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def collect_titleist_data(self):
        """タイトリストのデータを収集"""
        self.logger.info("タイトリストのデータ収集を開始")
        
        # メーカー情報の追加
        manufacturer_id = self.db.add_manufacturer({
            'name': 'Titleist',
            'country': 'USA',
            'website': 'https://www.titleist.com',
            'established_year': 1932,
            'notes': 'Titleist is a premium golf equipment manufacturer'
        })
        
        # ドライバーシリーズの収集
        self._collect_titleist_drivers(manufacturer_id)
        
        # アイアンシリーズの収集
        self._collect_titleist_irons(manufacturer_id)
        
        # ウェッジシリーズの収集
        self._collect_titleist_wedges(manufacturer_id)
        
    def _collect_titleist_drivers(self, manufacturer_id: int):
        """タイトリストのドライバー情報を収集"""
        url = "https://www.titleist.com/golf-clubs/drivers"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # シリーズ情報の取得
            series_data = {
                'manufacturer_id': manufacturer_id,
                'name': 'TSR Series',
                'release_year': 2023,
                'target_handicap_range': '0-20',
                'technology_description': 'Advanced aerodynamics and speed technologies',
                'notes': 'Latest driver series from Titleist'
            }
            series_id = self.db.add_club_series(series_data)
            
            # モデル情報の取得
            models = [
                {
                    'series_id': series_id,
                    'name': 'TSR1',
                    'club_type': 'driver',
                    'loft_range': [8.0, 9.0, 10.0, 11.0],
                    'stock_length_range': [45.0, 45.5],
                    'stock_weight_range': [195, 205],
                    'stock_swing_weight_range': ['D2', 'D4'],
                    'stock_shaft_options': ['HZRDUS Black', 'Tensei AV Blue'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 599.99,
                    'notes': 'Maximum forgiveness driver'
                },
                # 他のモデルも同様に追加
            ]
            
            for model in models:
                self.db.add_club_model(model)
                
        except Exception as e:
            self.logger.error(f"タイトリストドライバーのデータ収集中にエラーが発生: {e}")
            
    def _collect_titleist_irons(self, manufacturer_id: int):
        """タイトリストのアイアン情報を収集"""
        url = "https://www.titleist.com/golf-clubs/irons"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # シリーズ情報の取得
            series_data = {
                'manufacturer_id': manufacturer_id,
                'name': 'T-Series',
                'release_year': 2023,
                'target_handicap_range': '0-15',
                'technology_description': 'Progressive design and advanced materials',
                'notes': 'Latest iron series from Titleist'
            }
            series_id = self.db.add_club_series(series_data)
            
            # モデル情報の取得
            models = [
                {
                    'series_id': series_id,
                    'name': 'T100',
                    'club_type': 'iron',
                    'loft_range': [3, 4, 5, 6, 7, 8, 9, 'PW'],
                    'stock_length_range': [37.0, 38.5],
                    'stock_weight_range': [400, 420],
                    'stock_swing_weight_range': ['D2', 'D4'],
                    'stock_shaft_options': ['Dynamic Gold', 'Project X'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 199.99,
                    'notes': 'Players iron with forgiveness'
                },
                # 他のモデルも同様に追加
            ]
            
            for model in models:
                self.db.add_club_model(model)
                
        except Exception as e:
            self.logger.error(f"タイトリストアイアンのデータ収集中にエラーが発生: {e}")
            
    def _collect_titleist_wedges(self, manufacturer_id: int):
        """タイトリストのウェッジ情報を収集"""
        url = "https://www.titleist.com/golf-clubs/wedges"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # シリーズ情報の取得
            series_data = {
                'manufacturer_id': manufacturer_id,
                'name': 'Vokey Design',
                'release_year': 2023,
                'target_handicap_range': '0-20',
                'technology_description': 'Precision milled grooves and versatile grinds',
                'notes': 'Premium wedge series from Titleist'
            }
            series_id = self.db.add_club_series(series_data)
            
            # モデル情報の取得
            models = [
                {
                    'series_id': series_id,
                    'name': 'SM9',
                    'club_type': 'wedge',
                    'loft_range': [46, 48, 50, 52, 54, 56, 58, 60, 62],
                    'stock_length_range': [35.0, 35.5],
                    'stock_weight_range': [300, 320],
                    'stock_swing_weight_range': ['D3', 'D5'],
                    'stock_shaft_options': ['Dynamic Gold'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 179.99,
                    'notes': 'Tour-proven wedge design'
                },
                # 他のモデルも同様に追加
            ]
            
            for model in models:
                self.db.add_club_model(model)
                
        except Exception as e:
            self.logger.error(f"タイトリストウェッジのデータ収集中にエラーが発生: {e}")
            
    def collect_callaway_data(self):
        """キャロウェイのデータを収集"""
        self.logger.info("キャロウェイのデータ収集を開始")
        
        # メーカー情報の追加
        manufacturer_id = self.db.add_manufacturer({
            'name': 'Callaway',
            'country': 'USA',
            'website': 'https://www.callawaygolf.com',
            'established_year': 1982,
            'notes': 'Callaway is a leading golf equipment manufacturer'
        })
        
        # ドライバーシリーズの収集
        self._collect_callaway_drivers(manufacturer_id)
        
        # アイアンシリーズの収集
        self._collect_callaway_irons(manufacturer_id)
        
        # ウェッジシリーズの収集
        self._collect_callaway_wedges(manufacturer_id)
        
    def _collect_callaway_drivers(self, manufacturer_id: int):
        """キャロウェイのドライバー情報を収集"""
        url = "https://www.callawaygolf.com/golf-clubs/drivers"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # シリーズ情報の取得
            series_data = {
                'manufacturer_id': manufacturer_id,
                'name': 'Paradym Series',
                'release_year': 2023,
                'target_handicap_range': '0-20',
                'technology_description': 'AI-designed face and advanced materials',
                'notes': 'Latest driver series from Callaway'
            }
            series_id = self.db.add_club_series(series_data)
            
            # モデル情報の取得
            models = [
                {
                    'series_id': series_id,
                    'name': 'Paradym',
                    'club_type': 'driver',
                    'loft_range': [8.5, 9.0, 10.5, 12.0],
                    'stock_length_range': [45.5, 46.0],
                    'stock_weight_range': [200, 210],
                    'stock_swing_weight_range': ['D2', 'D4'],
                    'stock_shaft_options': ['Project X HZRDUS', 'Mitsubishi Tensei'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 599.99,
                    'notes': 'Tour-inspired driver with AI face design'
                },
                {
                    'series_id': series_id,
                    'name': 'Paradym X',
                    'club_type': 'driver',
                    'loft_range': [9.0, 10.5, 12.0],
                    'stock_length_range': [45.5, 46.0],
                    'stock_weight_range': [195, 205],
                    'stock_swing_weight_range': ['D1', 'D3'],
                    'stock_shaft_options': ['Project X HZRDUS', 'Mitsubishi Tensei'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 599.99,
                    'notes': 'Maximum forgiveness driver'
                }
            ]
            
            for model in models:
                self.db.add_club_model(model)
                
        except Exception as e:
            self.logger.error(f"キャロウェイドライバーのデータ収集中にエラーが発生: {e}")
            
    def _collect_callaway_irons(self, manufacturer_id: int):
        """キャロウェイのアイアン情報を収集"""
        url = "https://www.callawaygolf.com/golf-clubs/irons"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # シリーズ情報の取得
            series_data = {
                'manufacturer_id': manufacturer_id,
                'name': 'Apex Series',
                'release_year': 2023,
                'target_handicap_range': '0-15',
                'technology_description': 'Forged construction with AI face design',
                'notes': 'Premium iron series from Callaway'
            }
            series_id = self.db.add_club_series(series_data)
            
            # モデル情報の取得
            models = [
                {
                    'series_id': series_id,
                    'name': 'Apex Pro',
                    'club_type': 'iron',
                    'loft_range': [3, 4, 5, 6, 7, 8, 9, 'PW'],
                    'stock_length_range': [37.0, 38.5],
                    'stock_weight_range': [410, 430],
                    'stock_swing_weight_range': ['D2', 'D4'],
                    'stock_shaft_options': ['True Temper Dynamic Gold', 'Project X'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 199.99,
                    'notes': 'Tour-inspired forged iron'
                },
                {
                    'series_id': series_id,
                    'name': 'Apex',
                    'club_type': 'iron',
                    'loft_range': [4, 5, 6, 7, 8, 9, 'PW', 'AW'],
                    'stock_length_range': [37.0, 38.5],
                    'stock_weight_range': [400, 420],
                    'stock_swing_weight_range': ['D1', 'D3'],
                    'stock_shaft_options': ['True Temper Dynamic Gold', 'Project X'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 199.99,
                    'notes': 'Forged iron with forgiveness'
                }
            ]
            
            for model in models:
                self.db.add_club_model(model)
                
        except Exception as e:
            self.logger.error(f"キャロウェイアイアンのデータ収集中にエラーが発生: {e}")
            
    def _collect_callaway_wedges(self, manufacturer_id: int):
        """キャロウェイのウェッジ情報を収集"""
        url = "https://www.callawaygolf.com/golf-clubs/wedges"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # シリーズ情報の取得
            series_data = {
                'manufacturer_id': manufacturer_id,
                'name': 'Jaws Series',
                'release_year': 2023,
                'target_handicap_range': '0-20',
                'technology_description': 'Precision milled grooves and versatile grinds',
                'notes': 'Premium wedge series from Callaway'
            }
            series_id = self.db.add_club_series(series_data)
            
            # モデル情報の取得
            models = [
                {
                    'series_id': series_id,
                    'name': 'Jaws Raw',
                    'club_type': 'wedge',
                    'loft_range': [46, 48, 50, 52, 54, 56, 58, 60],
                    'stock_length_range': [35.0, 35.5],
                    'stock_weight_range': [310, 330],
                    'stock_swing_weight_range': ['D3', 'D5'],
                    'stock_shaft_options': ['True Temper Dynamic Gold'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 179.99,
                    'notes': 'Tour-proven wedge design'
                }
            ]
            
            for model in models:
                self.db.add_club_model(model)
                
        except Exception as e:
            self.logger.error(f"キャロウェイウェッジのデータ収集中にエラーが発生: {e}")
            
    def collect_taylormade_data(self):
        """テーラーメイドのデータを収集"""
        self.logger.info("テーラーメイドのデータ収集を開始")
        
        # メーカー情報の追加
        manufacturer_id = self.db.add_manufacturer({
            'name': 'TaylorMade',
            'country': 'USA',
            'website': 'https://www.taylormadegolf.com',
            'established_year': 1979,
            'notes': 'TaylorMade is a leading golf equipment manufacturer'
        })
        
        # ドライバーシリーズの収集
        self._collect_taylormade_drivers(manufacturer_id)
        
        # アイアンシリーズの収集
        self._collect_taylormade_irons(manufacturer_id)
        
        # ウェッジシリーズの収集
        self._collect_taylormade_wedges(manufacturer_id)
        
    def _collect_taylormade_drivers(self, manufacturer_id: int):
        """テーラーメイドのドライバー情報を収集"""
        url = "https://www.taylormadegolf.com/golf-clubs/drivers"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # シリーズ情報の取得
            series_data = {
                'manufacturer_id': manufacturer_id,
                'name': 'Stealth 2 Series',
                'release_year': 2023,
                'target_handicap_range': '0-20',
                'technology_description': 'Carbon face and advanced aerodynamics',
                'notes': 'Latest driver series from TaylorMade'
            }
            series_id = self.db.add_club_series(series_data)
            
            # モデル情報の取得
            models = [
                {
                    'series_id': series_id,
                    'name': 'Stealth 2 Plus',
                    'club_type': 'driver',
                    'loft_range': [8.0, 9.0, 10.5],
                    'stock_length_range': [45.5, 46.0],
                    'stock_weight_range': [195, 205],
                    'stock_swing_weight_range': ['D2', 'D4'],
                    'stock_shaft_options': ['Fujikura Ventus', 'Mitsubishi Tensei'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 599.99,
                    'notes': 'Tour-inspired driver with carbon face'
                },
                {
                    'series_id': series_id,
                    'name': 'Stealth 2',
                    'club_type': 'driver',
                    'loft_range': [9.0, 10.5, 12.0],
                    'stock_length_range': [45.5, 46.0],
                    'stock_weight_range': [190, 200],
                    'stock_swing_weight_range': ['D1', 'D3'],
                    'stock_shaft_options': ['Fujikura Ventus', 'Mitsubishi Tensei'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 599.99,
                    'notes': 'Maximum forgiveness driver'
                }
            ]
            
            for model in models:
                self.db.add_club_model(model)
                
        except Exception as e:
            self.logger.error(f"テーラーメイドドライバーのデータ収集中にエラーが発生: {e}")
            
    def _collect_taylormade_irons(self, manufacturer_id: int):
        """テーラーメイドのアイアン情報を収集"""
        url = "https://www.taylormadegolf.com/golf-clubs/irons"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # シリーズ情報の取得
            series_data = {
                'manufacturer_id': manufacturer_id,
                'name': 'P Series',
                'release_year': 2023,
                'target_handicap_range': '0-15',
                'technology_description': 'Forged construction with speed pocket',
                'notes': 'Premium iron series from TaylorMade'
            }
            series_id = self.db.add_club_series(series_data)
            
            # モデル情報の取得
            models = [
                {
                    'series_id': series_id,
                    'name': 'P7MC',
                    'club_type': 'iron',
                    'loft_range': [3, 4, 5, 6, 7, 8, 9, 'PW'],
                    'stock_length_range': [37.0, 38.5],
                    'stock_weight_range': [415, 435],
                    'stock_swing_weight_range': ['D2', 'D4'],
                    'stock_shaft_options': ['True Temper Dynamic Gold', 'Project X'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 199.99,
                    'notes': 'Tour-inspired forged iron'
                },
                {
                    'series_id': series_id,
                    'name': 'P790',
                    'club_type': 'iron',
                    'loft_range': [3, 4, 5, 6, 7, 8, 9, 'PW', 'AW'],
                    'stock_length_range': [37.0, 38.5],
                    'stock_weight_range': [405, 425],
                    'stock_swing_weight_range': ['D1', 'D3'],
                    'stock_shaft_options': ['True Temper Dynamic Gold', 'Project X'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 199.99,
                    'notes': 'Forged iron with speed pocket'
                }
            ]
            
            for model in models:
                self.db.add_club_model(model)
                
        except Exception as e:
            self.logger.error(f"テーラーメイドアイアンのデータ収集中にエラーが発生: {e}")
            
    def _collect_taylormade_wedges(self, manufacturer_id: int):
        """テーラーメイドのウェッジ情報を収集"""
        url = "https://www.taylormadegolf.com/golf-clubs/wedges"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # シリーズ情報の取得
            series_data = {
                'manufacturer_id': manufacturer_id,
                'name': 'MG Series',
                'release_year': 2023,
                'target_handicap_range': '0-20',
                'technology_description': 'Precision milled grooves and versatile grinds',
                'notes': 'Premium wedge series from TaylorMade'
            }
            series_id = self.db.add_club_series(series_data)
            
            # モデル情報の取得
            models = [
                {
                    'series_id': series_id,
                    'name': 'MG4',
                    'club_type': 'wedge',
                    'loft_range': [46, 48, 50, 52, 54, 56, 58, 60],
                    'stock_length_range': [35.0, 35.5],
                    'stock_weight_range': [305, 325],
                    'stock_swing_weight_range': ['D3', 'D5'],
                    'stock_shaft_options': ['True Temper Dynamic Gold'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 179.99,
                    'notes': 'Tour-proven wedge design'
                }
            ]
            
            for model in models:
                self.db.add_club_model(model)
                
        except Exception as e:
            self.logger.error(f"テーラーメイドウェッジのデータ収集中にエラーが発生: {e}")
            
    def collect_mizuno_data(self):
        """ミズノのデータを収集"""
        self.logger.info("ミズノのデータ収集を開始")
        
        # メーカー情報の追加
        manufacturer_id = self.db.add_manufacturer({
            'name': 'Mizuno',
            'country': 'Japan',
            'website': 'https://www.mizunogolf.com',
            'established_year': 1906,
            'notes': 'Mizuno is a premium Japanese golf equipment manufacturer'
        })
        
        # ドライバーシリーズの収集
        self._collect_mizuno_drivers(manufacturer_id)
        
        # アイアンシリーズの収集
        self._collect_mizuno_irons(manufacturer_id)
        
        # ウェッジシリーズの収集
        self._collect_mizuno_wedges(manufacturer_id)
        
    def _collect_mizuno_drivers(self, manufacturer_id: int):
        """ミズノのドライバー情報を収集"""
        url = "https://www.mizunogolf.com/golf-clubs/drivers"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # シリーズ情報の取得
            series_data = {
                'manufacturer_id': manufacturer_id,
                'name': 'ST Series',
                'release_year': 2023,
                'target_handicap_range': '0-20',
                'technology_description': 'Forged titanium face and wave technology',
                'notes': 'Latest driver series from Mizuno'
            }
            series_id = self.db.add_club_series(series_data)
            
            # モデル情報の取得
            models = [
                {
                    'series_id': series_id,
                    'name': 'ST-X 230',
                    'club_type': 'driver',
                    'loft_range': [9.0, 10.5, 12.0],
                    'stock_length_range': [45.5, 46.0],
                    'stock_weight_range': [195, 205],
                    'stock_swing_weight_range': ['D2', 'D4'],
                    'stock_shaft_options': ['Mitsubishi Tensei', 'Fujikura Ventus'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 549.99,
                    'notes': 'Maximum forgiveness driver'
                },
                {
                    'series_id': series_id,
                    'name': 'ST-Z 230',
                    'club_type': 'driver',
                    'loft_range': [8.5, 9.5, 10.5],
                    'stock_length_range': [45.5, 46.0],
                    'stock_weight_range': [190, 200],
                    'stock_swing_weight_range': ['D1', 'D3'],
                    'stock_shaft_options': ['Mitsubishi Tensei', 'Fujikura Ventus'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 549.99,
                    'notes': 'Tour-inspired driver'
                }
            ]
            
            for model in models:
                self.db.add_club_model(model)
                
        except Exception as e:
            self.logger.error(f"ミズノドライバーのデータ収集中にエラーが発生: {e}")
            
    def _collect_mizuno_irons(self, manufacturer_id: int):
        """ミズノのアイアン情報を収集"""
        url = "https://www.mizunogolf.com/golf-clubs/irons"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # シリーズ情報の取得
            series_data = {
                'manufacturer_id': manufacturer_id,
                'name': 'Pro Series',
                'release_year': 2023,
                'target_handicap_range': '0-15',
                'technology_description': 'Forged construction with grain flow forging',
                'notes': 'Premium iron series from Mizuno'
            }
            series_id = self.db.add_club_series(series_data)
            
            # モデル情報の取得
            models = [
                {
                    'series_id': series_id,
                    'name': 'MP-241',
                    'club_type': 'iron',
                    'loft_range': [3, 4, 5, 6, 7, 8, 9, 'PW'],
                    'stock_length_range': [37.0, 38.5],
                    'stock_weight_range': [415, 435],
                    'stock_swing_weight_range': ['D2', 'D4'],
                    'stock_shaft_options': ['True Temper Dynamic Gold', 'Project X'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 199.99,
                    'notes': 'Tour-inspired forged iron'
                },
                {
                    'series_id': series_id,
                    'name': 'JPX923 Tour',
                    'club_type': 'iron',
                    'loft_range': [4, 5, 6, 7, 8, 9, 'PW', 'GW'],
                    'stock_length_range': [37.0, 38.5],
                    'stock_weight_range': [405, 425],
                    'stock_swing_weight_range': ['D1', 'D3'],
                    'stock_shaft_options': ['True Temper Dynamic Gold', 'Project X'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 199.99,
                    'notes': 'Forged iron with forgiveness'
                }
            ]
            
            for model in models:
                self.db.add_club_model(model)
                
        except Exception as e:
            self.logger.error(f"ミズノアイアンのデータ収集中にエラーが発生: {e}")
            
    def _collect_mizuno_wedges(self, manufacturer_id: int):
        """ミズノのウェッジ情報を収集"""
        url = "https://www.mizunogolf.com/golf-clubs/wedges"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # シリーズ情報の取得
            series_data = {
                'manufacturer_id': manufacturer_id,
                'name': 'T Series',
                'release_year': 2023,
                'target_handicap_range': '0-20',
                'technology_description': 'Precision milled grooves and versatile grinds',
                'notes': 'Premium wedge series from Mizuno'
            }
            series_id = self.db.add_club_series(series_data)
            
            # モデル情報の取得
            models = [
                {
                    'series_id': series_id,
                    'name': 'T24',
                    'club_type': 'wedge',
                    'loft_range': [46, 48, 50, 52, 54, 56, 58, 60],
                    'stock_length_range': [35.0, 35.5],
                    'stock_weight_range': [305, 325],
                    'stock_swing_weight_range': ['D3', 'D5'],
                    'stock_shaft_options': ['True Temper Dynamic Gold'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 179.99,
                    'notes': 'Tour-proven wedge design'
                }
            ]
            
            for model in models:
                self.db.add_club_model(model)
                
        except Exception as e:
            self.logger.error(f"ミズノウェッジのデータ収集中にエラーが発生: {e}")
            
    def collect_ping_data(self):
        """ピンのデータを収集"""
        self.logger.info("ピンのデータ収集を開始")
        
        # メーカー情報の追加
        manufacturer_id = self.db.add_manufacturer({
            'name': 'PING',
            'country': 'USA',
            'website': 'https://www.ping.com',
            'established_year': 1959,
            'notes': 'PING is a leading golf equipment manufacturer known for custom fitting'
        })
        
        # ドライバーシリーズの収集
        self._collect_ping_drivers(manufacturer_id)
        
        # アイアンシリーズの収集
        self._collect_ping_irons(manufacturer_id)
        
        # ウェッジシリーズの収集
        self._collect_ping_wedges(manufacturer_id)
        
    def _collect_ping_drivers(self, manufacturer_id: int):
        """ピンのドライバー情報を収集"""
        url = "https://www.ping.com/golf-clubs/drivers"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # シリーズ情報の取得
            series_data = {
                'manufacturer_id': manufacturer_id,
                'name': 'G430 Series',
                'release_year': 2023,
                'target_handicap_range': '0-20',
                'technology_description': 'T9S+ titanium face and turbulator technology',
                'notes': 'Latest driver series from PING'
            }
            series_id = self.db.add_club_series(series_data)
            
            # モデル情報の取得
            models = [
                {
                    'series_id': series_id,
                    'name': 'G430 LST',
                    'club_type': 'driver',
                    'loft_range': [8.0, 9.0, 10.5],
                    'stock_length_range': [45.5, 46.0],
                    'stock_weight_range': [195, 205],
                    'stock_swing_weight_range': ['D2', 'D4'],
                    'stock_shaft_options': ['PING Tour', 'Aldila Rogue'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 599.99,
                    'notes': 'Low spin tour driver'
                },
                {
                    'series_id': series_id,
                    'name': 'G430 MAX',
                    'club_type': 'driver',
                    'loft_range': [9.0, 10.5, 12.0],
                    'stock_length_range': [45.5, 46.0],
                    'stock_weight_range': [190, 200],
                    'stock_swing_weight_range': ['D1', 'D3'],
                    'stock_shaft_options': ['PING Tour', 'Aldila Rogue'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 599.99,
                    'notes': 'Maximum forgiveness driver'
                }
            ]
            
            for model in models:
                self.db.add_club_model(model)
                
        except Exception as e:
            self.logger.error(f"ピンドライバーのデータ収集中にエラーが発生: {e}")
            
    def _collect_ping_irons(self, manufacturer_id: int):
        """ピンのアイアン情報を収集"""
        url = "https://www.ping.com/golf-clubs/irons"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # シリーズ情報の取得
            series_data = {
                'manufacturer_id': manufacturer_id,
                'name': 'i Series',
                'release_year': 2023,
                'target_handicap_range': '0-15',
                'technology_description': 'Forged construction with elastomer insert',
                'notes': 'Premium iron series from PING'
            }
            series_id = self.db.add_club_series(series_data)
            
            # モデル情報の取得
            models = [
                {
                    'series_id': series_id,
                    'name': 'i230',
                    'club_type': 'iron',
                    'loft_range': [3, 4, 5, 6, 7, 8, 9, 'PW'],
                    'stock_length_range': [37.0, 38.5],
                    'stock_weight_range': [415, 435],
                    'stock_swing_weight_range': ['D2', 'D4'],
                    'stock_shaft_options': ['True Temper Dynamic Gold', 'Project X'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 199.99,
                    'notes': 'Tour-inspired forged iron'
                },
                {
                    'series_id': series_id,
                    'name': 'i525',
                    'club_type': 'iron',
                    'loft_range': [4, 5, 6, 7, 8, 9, 'PW', 'UW'],
                    'stock_length_range': [37.0, 38.5],
                    'stock_weight_range': [405, 425],
                    'stock_swing_weight_range': ['D1', 'D3'],
                    'stock_shaft_options': ['True Temper Dynamic Gold', 'Project X'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 199.99,
                    'notes': 'Forged iron with forgiveness'
                }
            ]
            
            for model in models:
                self.db.add_club_model(model)
                
        except Exception as e:
            self.logger.error(f"ピンアイアンのデータ収集中にエラーが発生: {e}")
            
    def _collect_ping_wedges(self, manufacturer_id: int):
        """ピンのウェッジ情報を収集"""
        url = "https://www.ping.com/golf-clubs/wedges"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # シリーズ情報の取得
            series_data = {
                'manufacturer_id': manufacturer_id,
                'name': 'Glide Series',
                'release_year': 2023,
                'target_handicap_range': '0-20',
                'technology_description': 'Precision milled grooves and hydropearl finish',
                'notes': 'Premium wedge series from PING'
            }
            series_id = self.db.add_club_series(series_data)
            
            # モデル情報の取得
            models = [
                {
                    'series_id': series_id,
                    'name': 'Glide 4.0',
                    'club_type': 'wedge',
                    'loft_range': [46, 48, 50, 52, 54, 56, 58, 60],
                    'stock_length_range': [35.0, 35.5],
                    'stock_weight_range': [305, 325],
                    'stock_swing_weight_range': ['D3', 'D5'],
                    'stock_shaft_options': ['True Temper Dynamic Gold'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 179.99,
                    'notes': 'Tour-proven wedge design'
                }
            ]
            
            for model in models:
                self.db.add_club_model(model)
                
        except Exception as e:
            self.logger.error(f"ピンウェッジのデータ収集中にエラーが発生: {e}")
            
    def collect_srixon_data(self):
        """スリクソンのデータを収集"""
        self.logger.info("スリクソンのデータ収集を開始")
        
        # メーカー情報の追加
        manufacturer_id = self.db.add_manufacturer({
            'name': 'Srixon',
            'country': 'Japan',
            'website': 'https://www.srixon.com',
            'established_year': 1930,
            'notes': 'Srixon is a premium Japanese golf equipment manufacturer'
        })
        
        # ドライバーシリーズの収集
        self._collect_srixon_drivers(manufacturer_id)
        
        # アイアンシリーズの収集
        self._collect_srixon_irons(manufacturer_id)
        
        # ウェッジシリーズの収集
        self._collect_srixon_wedges(manufacturer_id)
        
    def _collect_srixon_drivers(self, manufacturer_id: int):
        """スリクソンのドライバー情報を収集"""
        url = "https://www.srixon.com/golf-clubs/drivers"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # シリーズ情報の取得
            series_data = {
                'manufacturer_id': manufacturer_id,
                'name': 'ZX Series',
                'release_year': 2023,
                'target_handicap_range': '0-20',
                'technology_description': 'Rebound frame and carbon crown technology',
                'notes': 'Latest driver series from Srixon'
            }
            series_id = self.db.add_club_series(series_data)
            
            # モデル情報の取得
            models = [
                {
                    'series_id': series_id,
                    'name': 'ZX5 LS',
                    'club_type': 'driver',
                    'loft_range': [8.5, 9.5, 10.5],
                    'stock_length_range': [45.5, 46.0],
                    'stock_weight_range': [195, 205],
                    'stock_swing_weight_range': ['D2', 'D4'],
                    'stock_shaft_options': ['Mitsubishi Tensei', 'Fujikura Ventus'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 549.99,
                    'notes': 'Low spin tour driver'
                },
                {
                    'series_id': series_id,
                    'name': 'ZX5',
                    'club_type': 'driver',
                    'loft_range': [9.0, 10.5, 12.0],
                    'stock_length_range': [45.5, 46.0],
                    'stock_weight_range': [190, 200],
                    'stock_swing_weight_range': ['D1', 'D3'],
                    'stock_shaft_options': ['Mitsubishi Tensei', 'Fujikura Ventus'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 549.99,
                    'notes': 'Maximum forgiveness driver'
                }
            ]
            
            for model in models:
                self.db.add_club_model(model)
                
        except Exception as e:
            self.logger.error(f"スリクソンドライバーのデータ収集中にエラーが発生: {e}")
            
    def _collect_srixon_irons(self, manufacturer_id: int):
        """スリクソンのアイアン情報を収集"""
        url = "https://www.srixon.com/golf-clubs/irons"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # シリーズ情報の取得
            series_data = {
                'manufacturer_id': manufacturer_id,
                'name': 'ZX Series',
                'release_year': 2023,
                'target_handicap_range': '0-15',
                'technology_description': 'Forged construction with mainframe technology',
                'notes': 'Premium iron series from Srixon'
            }
            series_id = self.db.add_club_series(series_data)
            
            # モデル情報の取得
            models = [
                {
                    'series_id': series_id,
                    'name': 'ZX7',
                    'club_type': 'iron',
                    'loft_range': [3, 4, 5, 6, 7, 8, 9, 'PW'],
                    'stock_length_range': [37.0, 38.5],
                    'stock_weight_range': [415, 435],
                    'stock_swing_weight_range': ['D2', 'D4'],
                    'stock_shaft_options': ['True Temper Dynamic Gold', 'Project X'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 199.99,
                    'notes': 'Tour-inspired forged iron'
                },
                {
                    'series_id': series_id,
                    'name': 'ZX5',
                    'club_type': 'iron',
                    'loft_range': [4, 5, 6, 7, 8, 9, 'PW', 'AW'],
                    'stock_length_range': [37.0, 38.5],
                    'stock_weight_range': [405, 425],
                    'stock_swing_weight_range': ['D1', 'D3'],
                    'stock_shaft_options': ['True Temper Dynamic Gold', 'Project X'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 199.99,
                    'notes': 'Forged iron with forgiveness'
                }
            ]
            
            for model in models:
                self.db.add_club_model(model)
                
        except Exception as e:
            self.logger.error(f"スリクソンアイアンのデータ収集中にエラーが発生: {e}")
            
    def _collect_srixon_wedges(self, manufacturer_id: int):
        """スリクソンのウェッジ情報を収集"""
        url = "https://www.srixon.com/golf-clubs/wedges"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # シリーズ情報の取得
            series_data = {
                'manufacturer_id': manufacturer_id,
                'name': 'ZX Series',
                'release_year': 2023,
                'target_handicap_range': '0-20',
                'technology_description': 'Precision milled grooves and versatile grinds',
                'notes': 'Premium wedge series from Srixon'
            }
            series_id = self.db.add_club_series(series_data)
            
            # モデル情報の取得
            models = [
                {
                    'series_id': series_id,
                    'name': 'ZX5',
                    'club_type': 'wedge',
                    'loft_range': [46, 48, 50, 52, 54, 56, 58, 60],
                    'stock_length_range': [35.0, 35.5],
                    'stock_weight_range': [305, 325],
                    'stock_swing_weight_range': ['D3', 'D5'],
                    'stock_shaft_options': ['True Temper Dynamic Gold'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 179.99,
                    'notes': 'Tour-proven wedge design'
                }
            ]
            
            for model in models:
                self.db.add_club_model(model)
                
        except Exception as e:
            self.logger.error(f"スリクソンウェッジのデータ収集中にエラーが発生: {e}")
            
    def collect_bridgestone_data(self):
        """ブリヂストンのデータを収集"""
        self.logger.info("ブリヂストンのデータ収集を開始")
        
        # メーカー情報の追加
        manufacturer_id = self.db.add_manufacturer({
            'name': 'Bridgestone',
            'country': 'Japan',
            'website': 'https://www.bridgestonegolf.com',
            'established_year': 1931,
            'notes': 'Bridgestone is a premium Japanese golf equipment manufacturer'
        })
        
        # ドライバーシリーズの収集
        self._collect_bridgestone_drivers(manufacturer_id)
        
        # アイアンシリーズの収集
        self._collect_bridgestone_irons(manufacturer_id)
        
        # ウェッジシリーズの収集
        self._collect_bridgestone_wedges(manufacturer_id)
        
    def _collect_bridgestone_drivers(self, manufacturer_id: int):
        """ブリヂストンのドライバー情報を収集"""
        url = "https://www.bridgestonegolf.com/golf-clubs/drivers"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # シリーズ情報の取得
            series_data = {
                'manufacturer_id': manufacturer_id,
                'name': 'Tour B Series',
                'release_year': 2023,
                'target_handicap_range': '0-20',
                'technology_description': 'Dual carbon crown and power rib technology',
                'notes': 'Latest driver series from Bridgestone'
            }
            series_id = self.db.add_club_series(series_data)
            
            # モデル情報の取得
            models = [
                {
                    'series_id': series_id,
                    'name': 'Tour B XD-7',
                    'club_type': 'driver',
                    'loft_range': [8.5, 9.5, 10.5],
                    'stock_length_range': [45.5, 46.0],
                    'stock_weight_range': [195, 205],
                    'stock_swing_weight_range': ['D2', 'D4'],
                    'stock_shaft_options': ['Mitsubishi Tensei', 'Fujikura Ventus'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 549.99,
                    'notes': 'Tour-inspired driver'
                },
                {
                    'series_id': series_id,
                    'name': 'Tour B XD-5',
                    'club_type': 'driver',
                    'loft_range': [9.0, 10.5, 12.0],
                    'stock_length_range': [45.5, 46.0],
                    'stock_weight_range': [190, 200],
                    'stock_swing_weight_range': ['D1', 'D3'],
                    'stock_shaft_options': ['Mitsubishi Tensei', 'Fujikura Ventus'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 549.99,
                    'notes': 'Maximum forgiveness driver'
                }
            ]
            
            for model in models:
                self.db.add_club_model(model)
                
        except Exception as e:
            self.logger.error(f"ブリヂストンドライバーのデータ収集中にエラーが発生: {e}")
            
    def _collect_bridgestone_irons(self, manufacturer_id: int):
        """ブリヂストンのアイアン情報を収集"""
        url = "https://www.bridgestonegolf.com/golf-clubs/irons"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # シリーズ情報の取得
            series_data = {
                'manufacturer_id': manufacturer_id,
                'name': 'Tour B Series',
                'release_year': 2023,
                'target_handicap_range': '0-15',
                'technology_description': 'Forged construction with power rib technology',
                'notes': 'Premium iron series from Bridgestone'
            }
            series_id = self.db.add_club_series(series_data)
            
            # モデル情報の取得
            models = [
                {
                    'series_id': series_id,
                    'name': 'Tour B X-CB',
                    'club_type': 'iron',
                    'loft_range': [3, 4, 5, 6, 7, 8, 9, 'PW'],
                    'stock_length_range': [37.0, 38.5],
                    'stock_weight_range': [415, 435],
                    'stock_swing_weight_range': ['D2', 'D4'],
                    'stock_shaft_options': ['True Temper Dynamic Gold', 'Project X'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 199.99,
                    'notes': 'Tour-inspired forged iron'
                },
                {
                    'series_id': series_id,
                    'name': 'Tour B X-CB',
                    'club_type': 'iron',
                    'loft_range': [4, 5, 6, 7, 8, 9, 'PW', 'AW'],
                    'stock_length_range': [37.0, 38.5],
                    'stock_weight_range': [405, 425],
                    'stock_swing_weight_range': ['D1', 'D3'],
                    'stock_shaft_options': ['True Temper Dynamic Gold', 'Project X'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 199.99,
                    'notes': 'Forged iron with forgiveness'
                }
            ]
            
            for model in models:
                self.db.add_club_model(model)
                
        except Exception as e:
            self.logger.error(f"ブリヂストンアイアンのデータ収集中にエラーが発生: {e}")
            
    def _collect_bridgestone_wedges(self, manufacturer_id: int):
        """ブリヂストンのウェッジ情報を収集"""
        url = "https://www.bridgestonegolf.com/golf-clubs/wedges"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # シリーズ情報の取得
            series_data = {
                'manufacturer_id': manufacturer_id,
                'name': 'Tour B Series',
                'release_year': 2023,
                'target_handicap_range': '0-20',
                'technology_description': 'Precision milled grooves and versatile grinds',
                'notes': 'Premium wedge series from Bridgestone'
            }
            series_id = self.db.add_club_series(series_data)
            
            # モデル情報の取得
            models = [
                {
                    'series_id': series_id,
                    'name': 'Tour B XW-1',
                    'club_type': 'wedge',
                    'loft_range': [46, 48, 50, 52, 54, 56, 58, 60],
                    'stock_length_range': [35.0, 35.5],
                    'stock_weight_range': [305, 325],
                    'stock_swing_weight_range': ['D3', 'D5'],
                    'stock_shaft_options': ['True Temper Dynamic Gold'],
                    'stock_grip_options': ['Golf Pride Tour Velvet'],
                    'release_year': 2023,
                    'msrp': 179.99,
                    'notes': 'Tour-proven wedge design'
                }
            ]
            
            for model in models:
                self.db.add_club_model(model)
                
        except Exception as e:
            self.logger.error(f"ブリヂストンウェッジのデータ収集中にエラーが発生: {e}")
            
    def collect_all_data(self):
        """全てのメーカーのデータを収集"""
        self.logger.info("全メーカーのデータ収集を開始")
        
        collectors = [
            self.collect_titleist_data,
            self.collect_callaway_data,
            self.collect_taylormade_data,
            self.collect_mizuno_data,
            self.collect_ping_data,
            self.collect_srixon_data,
            self.collect_bridgestone_data
        ]
        
        for collector in collectors:
            try:
                collector()
                # リクエスト間隔をランダムに設定
                time.sleep(random.uniform(2, 5))
            except Exception as e:
                self.logger.error(f"データ収集中にエラーが発生: {e}")
                continue
                
    def close(self):
        """データベース接続を閉じる"""
        self.db.close()
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 