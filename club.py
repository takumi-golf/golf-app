import numpy as np
from typing import Dict, List, Optional, Tuple, Union
import json
import os
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class MaintenanceType(Enum):
    """メンテナンスの種類"""
    GRIP_CHANGE = "グリップ交換"
    SHAFT_CHANGE = "シャフト交換"
    LOFT_ADJUSTMENT = "ロフト調整"
    LIE_ADJUSTMENT = "ライ角調整"
    WEIGHT_CHANGE = "重量調整"
    CLEANING = "清掃"
    REPAIR = "修理"
    OTHER = "その他"

@dataclass
class PerformanceData:
    """クラブの性能データ"""
    carry_distance: float  # キャリー距離（ヤード）
    total_distance: float  # トータル距離（ヤード）
    launch_angle: float    # 打ち出し角（度）
    spin_rate: float       # スピン量（rpm）
    ball_speed: float      # ボール初速（mph）
    club_speed: float      # クラブヘッドスピード（mph）
    smash_factor: float    # スマッシュファクター
    dispersion: float      # 方向性（ヤード）
    peak_height: float     # 最高到達点（ヤード）
    descent_angle: float   # 落下角（度）
    date: datetime         # 計測日時
    conditions: Dict[str, str]  # 計測条件（天候、気温、湿度など）
    notes: str             # 備考

@dataclass
class MaintenanceRecord:
    """メンテナンス記録"""
    date: datetime
    type: MaintenanceType
    description: str
    cost: float
    shop: str
    notes: str = ""

@dataclass
class UsageRecord:
    """使用記録"""
    date: datetime
    course: str
    weather: str
    temperature: float
    humidity: float
    shots: int
    notes: str = ""

class Club:
    """ゴルフクラブの基本クラス"""
    
    def __init__(
        self,
        name: str,
        loft: float,
        length: float,
        weight: float,
        shaft_flex: str,
        head_material: str,
        shaft_material: str,
        grip_type: str,
        manufacturer: str,
        model: str,
        year: int,
        price: float,
        condition: str,
        notes: str = "",
    ):
        self.name = name
        self.loft = loft
        self.length = length
        self.weight = weight
        self.shaft_flex = shaft_flex
        self.head_material = head_material
        self.shaft_material = shaft_material
        self.grip_type = grip_type
        self.manufacturer = manufacturer
        self.model = model
        self.year = year
        self.price = price
        self.condition = condition
        self.notes = notes
        self.performance_data: List[PerformanceData] = []
        self.recommended_settings: Dict = {}
        self.replacement_recommendation: Dict = {}
        self.maintenance_history: List[MaintenanceRecord] = []
        self.usage_history: List[UsageRecord] = []
        
    def add_performance_data(self, data: PerformanceData) -> None:
        """性能データを追加"""
        self.performance_data.append(data)
        self._update_recommended_settings()
        self._update_replacement_recommendation()
        
    def add_maintenance_record(self, record: MaintenanceRecord) -> None:
        """メンテナンス記録を追加"""
        self.maintenance_history.append(record)
        self._update_condition()
        
    def add_usage_record(self, record: UsageRecord) -> None:
        """使用記録を追加"""
        self.usage_history.append(record)
        
    def _update_recommended_settings(self) -> None:
        """推奨設定を更新"""
        if not self.performance_data:
            return
            
        # 平均性能データを取得
        avg_perf = self.get_average_performance()
        if not avg_perf:
            return
            
        # クラブタイプに基づく推奨設定
        club_type = self._determine_club_type()
        
        # 基本設定
        self.recommended_settings = {
            "club_type": club_type,
            "optimal_loft": self._calculate_optimal_loft(avg_perf),
            "optimal_length": self._calculate_optimal_length(avg_perf),
            "optimal_weight": self._calculate_optimal_weight(avg_perf),
            "recommended_shaft_flex": self._recommend_shaft_flex(avg_perf),
            "recommended_grip_size": self._recommend_grip_size(),
            "ball_position": self._recommend_ball_position(club_type),
            "stance_width": self._recommend_stance_width(club_type),
            "swing_tempo": self._recommend_swing_tempo(avg_perf),
            "launch_angle_target": self._calculate_launch_angle_target(avg_perf),
            "spin_rate_target": self._calculate_spin_rate_target(avg_perf),
            "notes": []
        }
        
        # パフォーマンスに基づく追加の推奨事項
        self._add_performance_based_recommendations(avg_perf)
        
    def _update_replacement_recommendation(self) -> None:
        """交換提案を更新"""
        current_year = datetime.now().year
        years_old = current_year - self.year
        
        # 基本情報
        self.replacement_recommendation = {
            "years_old": years_old,
            "condition_score": self._calculate_condition_score(),
            "performance_score": self._calculate_performance_score(),
            "technology_score": self._calculate_technology_score(),
            "recommendation": "交換不要",
            "reasons": [],
            "suggested_models": []
        }
        
        # 交換を推奨する条件をチェック
        self._check_replacement_conditions()
        
    def _calculate_condition_score(self) -> float:
        """状態スコアを計算"""
        condition_scores = {
            "新品": 1.0,
            "良好": 0.8,
            "普通": 0.6,
            "悪い": 0.4,
            "非常に悪い": 0.2
        }
        return condition_scores.get(self.condition, 0.5)
        
    def _calculate_performance_score(self) -> float:
        """性能スコアを計算"""
        if not self.performance_data:
            return 0.5
            
        avg_perf = self.get_average_performance()
        if not avg_perf:
            return 0.5
            
        # 各指標のスコアを計算
        scores = []
        
        # 距離のスコア
        club_type = self._determine_club_type()
        distance_targets = {
            "driver": 220,
            "wood": 200,
            "hybrid": 180,
            "iron": 160,
            "wedge": 100
        }
        target_distance = distance_targets.get(club_type, 150)
        distance_score = min(1.0, avg_perf["total_distance"] / target_distance)
        scores.append(distance_score)
        
        # 方向性のスコア
        dispersion_score = max(0.0, 1.0 - (avg_perf["dispersion"] / 30.0))
        scores.append(dispersion_score)
        
        # スピン量のスコア
        target_spin = self._calculate_spin_rate_target(avg_perf)
        spin_score = 1.0 - abs(avg_perf["spin_rate"] - target_spin) / target_spin
        scores.append(max(0.0, min(1.0, spin_score)))
        
        # 打ち出し角のスコア
        target_launch = self._calculate_launch_angle_target(avg_perf)
        launch_score = 1.0 - abs(avg_perf["launch_angle"] - target_launch) / target_launch
        scores.append(max(0.0, min(1.0, launch_score)))
        
        # 平均スコアを計算
        return sum(scores) / len(scores)
        
    def _calculate_technology_score(self) -> float:
        """技術革新スコアを計算"""
        current_year = datetime.now().year
        years_old = current_year - self.year
        
        # 年数に基づく技術革新の影響を計算
        if years_old <= 2:
            return 1.0
        elif years_old <= 5:
            return 0.8
        elif years_old <= 8:
            return 0.6
        elif years_old <= 10:
            return 0.4
        else:
            return 0.2
            
    def _check_replacement_conditions(self) -> None:
        """交換を推奨する条件をチェック"""
        # 年数チェック
        if self.replacement_recommendation["years_old"] >= 10:
            self.replacement_recommendation["recommendation"] = "交換推奨"
            self.replacement_recommendation["reasons"].append(
                f"クラブが{self.replacement_recommendation['years_old']}年経過しています。"
            )
            
        # 状態チェック
        if self.replacement_recommendation["condition_score"] < 0.4:
            self.replacement_recommendation["recommendation"] = "交換推奨"
            self.replacement_recommendation["reasons"].append(
                "クラブの状態が悪化しています。"
            )
            
        # 性能チェック
        if self.replacement_recommendation["performance_score"] < 0.6:
            self.replacement_recommendation["recommendation"] = "交換検討"
            self.replacement_recommendation["reasons"].append(
                "性能が低下しています。"
            )
            
        # 技術革新チェック
        if self.replacement_recommendation["technology_score"] < 0.4:
            self.replacement_recommendation["recommendation"] = "交換検討"
            self.replacement_recommendation["reasons"].append(
                "最新技術の恩恵を受けられていません。"
            )
            
        # 推奨モデルの提案
        if self.replacement_recommendation["recommendation"] != "交換不要":
            self._suggest_replacement_models()
            
    def _suggest_replacement_models(self) -> None:
        """交換推奨モデルを提案"""
        club_type = self._determine_club_type()
        
        # メーカーごとの最新モデル（仮のデータ）
        latest_models = {
            "driver": {
                "Titleist": "TSi3",
                "Callaway": "Rogue ST",
                "TaylorMade": "Stealth",
                "Ping": "G425",
                "Mizuno": "ST-Z"
            },
            "wood": {
                "Titleist": "TSi2",
                "Callaway": "Rogue ST",
                "TaylorMade": "Stealth",
                "Ping": "G425",
                "Mizuno": "ST-Z"
            },
            "iron": {
                "Titleist": "T200",
                "Callaway": "Apex",
                "TaylorMade": "P790",
                "Ping": "i525",
                "Mizuno": "JPX921"
            },
            "wedge": {
                "Titleist": "Vokey SM9",
                "Callaway": "Jaws",
                "TaylorMade": "MG3",
                "Ping": "Glide 4.0",
                "Mizuno": "T22"
            }
        }
        
        # 同じメーカーの最新モデルを提案
        if club_type in latest_models and self.manufacturer in latest_models[club_type]:
            self.replacement_recommendation["suggested_models"].append({
                "manufacturer": self.manufacturer,
                "model": latest_models[club_type][self.manufacturer],
                "reason": "同じメーカーの最新モデル"
            })
            
        # 他メーカーの人気モデルも提案
        for manufacturer, model in latest_models[club_type].items():
            if manufacturer != self.manufacturer:
                self.replacement_recommendation["suggested_models"].append({
                    "manufacturer": manufacturer,
                    "model": model,
                    "reason": "人気の最新モデル"
                })
                
    def get_recommended_settings(self) -> Dict:
        """推奨設定を取得"""
        if not self.recommended_settings:
            self._update_recommended_settings()
        return self.recommended_settings
        
    def get_latest_performance(self) -> Optional[PerformanceData]:
        """最新の性能データを取得"""
        if not self.performance_data:
            return None
        return max(self.performance_data, key=lambda x: x.date)
        
    def get_average_performance(self) -> Optional[Dict]:
        """平均性能データを計算"""
        if not self.performance_data:
            return None
            
        return {
            "carry_distance": np.mean([d.carry_distance for d in self.performance_data]),
            "total_distance": np.mean([d.total_distance for d in self.performance_data]),
            "launch_angle": np.mean([d.launch_angle for d in self.performance_data]),
            "spin_rate": np.mean([d.spin_rate for d in self.performance_data]),
            "ball_speed": np.mean([d.ball_speed for d in self.performance_data]),
            "club_speed": np.mean([d.club_speed for d in self.performance_data]),
            "smash_factor": np.mean([d.smash_factor for d in self.performance_data]),
            "dispersion": np.mean([d.dispersion for d in self.performance_data]),
            "peak_height": np.mean([d.peak_height for d in self.performance_data]),
            "descent_angle": np.mean([d.descent_angle for d in self.performance_data]),
            "data_points": len(self.performance_data)
        }
        
    def get_performance_trend(self, metric: str) -> List[Tuple[datetime, float]]:
        """特定の性能指標の推移を取得"""
        if not self.performance_data:
            return []
            
        if not hasattr(PerformanceData, metric):
            return []
            
        return [(d.date, getattr(d, metric)) for d in sorted(self.performance_data, key=lambda x: x.date)]
        
    def to_dict(self) -> Dict:
        """クラブの情報を辞書形式で返す"""
        return {
            "name": self.name,
            "loft": self.loft,
            "length": self.length,
            "weight": self.weight,
            "shaft_flex": self.shaft_flex,
            "head_material": self.head_material,
            "shaft_material": self.shaft_material,
            "grip_type": self.grip_type,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "year": self.year,
            "price": self.price,
            "condition": self.condition,
            "notes": self.notes,
            "performance_data": [
                {
                    "carry_distance": d.carry_distance,
                    "total_distance": d.total_distance,
                    "launch_angle": d.launch_angle,
                    "spin_rate": d.spin_rate,
                    "ball_speed": d.ball_speed,
                    "club_speed": d.club_speed,
                    "smash_factor": d.smash_factor,
                    "dispersion": d.dispersion,
                    "peak_height": d.peak_height,
                    "descent_angle": d.descent_angle,
                    "date": d.date.isoformat(),
                    "conditions": d.conditions,
                    "notes": d.notes
                }
                for d in self.performance_data
            ],
            "maintenance_history": [
                {
                    "date": record.date.isoformat(),
                    "type": record.type.value,
                    "description": record.description,
                    "cost": record.cost,
                    "shop": record.shop,
                    "notes": record.notes
                }
                for record in self.maintenance_history
            ],
            "usage_history": [
                {
                    "date": record.date.isoformat(),
                    "course": record.course,
                    "weather": record.weather,
                    "temperature": record.temperature,
                    "humidity": record.humidity,
                    "shots": record.shots,
                    "notes": record.notes
                }
                for record in self.usage_history
            ]
        }
        
    @classmethod
    def from_dict(cls, data: Dict) -> 'Club':
        """辞書からクラブオブジェクトを作成"""
        club = cls(
            name=data["name"],
            loft=data["loft"],
            length=data["length"],
            weight=data["weight"],
            shaft_flex=data["shaft_flex"],
            head_material=data["head_material"],
            shaft_material=data["shaft_material"],
            grip_type=data["grip_type"],
            manufacturer=data["manufacturer"],
            model=data["model"],
            year=data["year"],
            price=data["price"],
            condition=data["condition"],
            notes=data.get("notes", "")
        )
        
        # 性能データの復元
        for perf_data in data.get("performance_data", []):
            club.add_performance_data(PerformanceData(
                carry_distance=perf_data["carry_distance"],
                total_distance=perf_data["total_distance"],
                launch_angle=perf_data["launch_angle"],
                spin_rate=perf_data["spin_rate"],
                ball_speed=perf_data["ball_speed"],
                club_speed=perf_data["club_speed"],
                smash_factor=perf_data["smash_factor"],
                dispersion=perf_data["dispersion"],
                peak_height=perf_data["peak_height"],
                descent_angle=perf_data["descent_angle"],
                date=datetime.fromisoformat(perf_data["date"]),
                conditions=perf_data["conditions"],
                notes=perf_data["notes"]
            ))
            
        # メンテナンス履歴の復元
        for maint_data in data.get("maintenance_history", []):
            club.add_maintenance_record(MaintenanceRecord(
                date=datetime.fromisoformat(maint_data["date"]),
                type=MaintenanceType(maint_data["type"]),
                description=maint_data["description"],
                cost=maint_data["cost"],
                shop=maint_data["shop"],
                notes=maint_data["notes"]
            ))
            
        # 使用履歴の復元
        for usage_data in data.get("usage_history", []):
            club.add_usage_record(UsageRecord(
                date=datetime.fromisoformat(usage_data["date"]),
                course=usage_data["course"],
                weather=usage_data["weather"],
                temperature=usage_data["temperature"],
                humidity=usage_data["humidity"],
                shots=usage_data["shots"],
                notes=usage_data["notes"]
            ))
            
        return club
        
    def __str__(self) -> str:
        return f"{self.manufacturer} {self.model} ({self.year}) - {self.name}"
        
    def __repr__(self) -> str:
        return f"Club({self.name}, {self.loft}°, {self.length}in, {self.weight}g)"

    def get_replacement_recommendation(self) -> Dict:
        """交換提案を取得"""
        if not self.replacement_recommendation:
            self._update_replacement_recommendation()
        return self.replacement_recommendation

    def _update_condition(self) -> None:
        """状態を更新"""
        if not self.maintenance_history:
            return
            
        # 最新のメンテナンス記録を取得
        latest_maintenance = max(self.maintenance_history, key=lambda x: x.date)
        
        # メンテナンスの種類に応じて状態を更新
        if latest_maintenance.type == MaintenanceType.GRIP_CHANGE:
            self.grip_type = latest_maintenance.description
        elif latest_maintenance.type == MaintenanceType.SHAFT_CHANGE:
            self.shaft_flex = latest_maintenance.description
        elif latest_maintenance.type == MaintenanceType.LOFT_ADJUSTMENT:
            self.loft = float(latest_maintenance.description)
        elif latest_maintenance.type == MaintenanceType.LIE_ADJUSTMENT:
            # ライ角の調整は別の属性として管理する必要がある
            pass
        elif latest_maintenance.type == MaintenanceType.WEIGHT_CHANGE:
            self.weight = float(latest_maintenance.description)
            
    def get_maintenance_summary(self) -> Dict:
        """メンテナンス履歴のサマリーを取得"""
        if not self.maintenance_history:
            return {"total_records": 0}
            
        summary = {
            "total_records": len(self.maintenance_history),
            "total_cost": sum(record.cost for record in self.maintenance_history),
            "by_type": {},
            "by_shop": {},
            "latest_maintenance": None
        }
        
        # メンテナンスタイプごとの集計
        for record in self.maintenance_history:
            summary["by_type"][record.type.value] = summary["by_type"].get(record.type.value, 0) + 1
            summary["by_shop"][record.shop] = summary["by_shop"].get(record.shop, 0) + 1
            
        # 最新のメンテナンス記録
        latest = max(self.maintenance_history, key=lambda x: x.date)
        summary["latest_maintenance"] = {
            "date": latest.date.isoformat(),
            "type": latest.type.value,
            "description": latest.description,
            "shop": latest.shop
        }
        
        return summary
        
    def get_usage_summary(self) -> Dict:
        """使用履歴のサマリーを取得"""
        if not self.usage_history:
            return {"total_records": 0}
            
        summary = {
            "total_records": len(self.usage_history),
            "total_shots": sum(record.shots for record in self.usage_history),
            "by_course": {},
            "by_weather": {},
            "average_temperature": np.mean([record.temperature for record in self.usage_history]),
            "average_humidity": np.mean([record.humidity for record in self.usage_history]),
            "latest_usage": None
        }
        
        # コースと天候ごとの集計
        for record in self.usage_history:
            summary["by_course"][record.course] = summary["by_course"].get(record.course, 0) + 1
            summary["by_weather"][record.weather] = summary["by_weather"].get(record.weather, 0) + 1
            
        # 最新の使用記録
        latest = max(self.usage_history, key=lambda x: x.date)
        summary["latest_usage"] = {
            "date": latest.date.isoformat(),
            "course": latest.course,
            "weather": latest.weather,
            "shots": latest.shots
        }
        
        return summary
        
    def get_maintenance_schedule(self) -> Dict:
        """メンテナンススケジュールを取得"""
        if not self.maintenance_history:
            return {"next_maintenance": None}
            
        # 最新のメンテナンス記録を取得
        latest_maintenance = max(self.maintenance_history, key=lambda x: x.date)
        days_since_last_maintenance = (datetime.now() - latest_maintenance.date).days
        
        schedule = {
            "days_since_last_maintenance": days_since_last_maintenance,
            "next_maintenance": None,
            "recommendations": []
        }
        
        # グリップ交換の推奨（1年ごと）
        if days_since_last_maintenance >= 365:
            schedule["recommendations"].append({
                "type": MaintenanceType.GRIP_CHANGE.value,
                "reason": "グリップの交換時期です",
                "priority": "high"
            })
            
        # シャフトの点検（2年ごと）
        if days_since_last_maintenance >= 730:
            schedule["recommendations"].append({
                "type": MaintenanceType.SHAFT_CHANGE.value,
                "reason": "シャフトの点検時期です",
                "priority": "medium"
            })
            
        # ロフト角の確認（6ヶ月ごと）
        if days_since_last_maintenance >= 180:
            schedule["recommendations"].append({
                "type": MaintenanceType.LOFT_ADJUSTMENT.value,
                "reason": "ロフト角の確認時期です",
                "priority": "low"
            })
            
        # 次のメンテナンス予定を設定
        if schedule["recommendations"]:
            next_maintenance = min(
                (rec for rec in schedule["recommendations"] if rec["priority"] == "high"),
                key=lambda x: x["type"],
                default=schedule["recommendations"][0]
            )
            schedule["next_maintenance"] = next_maintenance
            
        return schedule

    def analyze_performance_correlations(self) -> Dict:
        """パフォーマンスデータと使用履歴の相関分析"""
        if not self.performance_data or not self.usage_history:
            return {"error": "分析に必要なデータが不足しています"}
            
        # 日付でソート
        sorted_perf = sorted(self.performance_data, key=lambda x: x.date)
        sorted_usage = sorted(self.usage_history, key=lambda x: x.date)
        
        # 使用回数とパフォーマンスの相関
        usage_counts = {}
        for record in sorted_usage:
            date = record.date.date()
            usage_counts[date] = usage_counts.get(date, 0) + record.shots
            
        # パフォーマンス指標ごとの相関分析
        correlations = {
            "carry_distance": self._calculate_correlation(usage_counts, sorted_perf, "carry_distance"),
            "total_distance": self._calculate_correlation(usage_counts, sorted_perf, "total_distance"),
            "launch_angle": self._calculate_correlation(usage_counts, sorted_perf, "launch_angle"),
            "spin_rate": self._calculate_correlation(usage_counts, sorted_perf, "spin_rate"),
            "ball_speed": self._calculate_correlation(usage_counts, sorted_perf, "ball_speed"),
            "club_speed": self._calculate_correlation(usage_counts, sorted_perf, "club_speed"),
            "smash_factor": self._calculate_correlation(usage_counts, sorted_perf, "smash_factor"),
            "dispersion": self._calculate_correlation(usage_counts, sorted_perf, "dispersion")
        }
        
        # 天候とパフォーマンスの相関
        weather_correlations = self._analyze_weather_correlations(sorted_perf, sorted_usage)
        
        # コースごとのパフォーマンス分析
        course_performance = self._analyze_course_performance(sorted_perf, sorted_usage)
        
        return {
            "usage_correlations": correlations,
            "weather_correlations": weather_correlations,
            "course_performance": course_performance,
            "recommendations": self._generate_correlation_recommendations(correlations, weather_correlations)
        }
        
    def _calculate_correlation(self, usage_counts: Dict, perf_data: List[PerformanceData], metric: str) -> Dict:
        """使用回数と特定のパフォーマンス指標の相関を計算"""
        # 使用回数とパフォーマンス指標のデータを準備
        usage_values = []
        perf_values = []
        
        for perf in perf_data:
            date = perf.date.date()
            if date in usage_counts:
                usage_values.append(usage_counts[date])
                perf_values.append(getattr(perf, metric))
                
        if not usage_values or not perf_values:
            return {"correlation": None, "trend": None}
            
        # 相関係数を計算
        correlation = np.corrcoef(usage_values, perf_values)[0, 1]
        
        # トレンドを計算
        if len(perf_values) > 1:
            trend = np.polyfit(range(len(perf_values)), perf_values, 1)[0]
        else:
            trend = None
            
        return {
            "correlation": float(correlation) if not np.isnan(correlation) else None,
            "trend": float(trend) if trend is not None else None,
            "interpretation": self._interpret_correlation(correlation, trend)
        }
        
    def _analyze_weather_correlations(self, perf_data: List[PerformanceData], usage_data: List[UsageRecord]) -> Dict:
        """天候とパフォーマンスの相関分析"""
        weather_performance = {}
        
        for perf in perf_data:
            # 同じ日付の使用記録を探す
            matching_usage = [u for u in usage_data if u.date.date() == perf.date.date()]
            if matching_usage:
                weather = matching_usage[0].weather
                if weather not in weather_performance:
                    weather_performance[weather] = {
                        "count": 0,
                        "carry_distance": [],
                        "total_distance": [],
                        "launch_angle": [],
                        "spin_rate": []
                    }
                    
                weather_performance[weather]["count"] += 1
                weather_performance[weather]["carry_distance"].append(perf.carry_distance)
                weather_performance[weather]["total_distance"].append(perf.total_distance)
                weather_performance[weather]["launch_angle"].append(perf.launch_angle)
                weather_performance[weather]["spin_rate"].append(perf.spin_rate)
                
        # 各天候ごとの平均値を計算
        for weather in weather_performance:
            for metric in ["carry_distance", "total_distance", "launch_angle", "spin_rate"]:
                if weather_performance[weather][metric]:
                    weather_performance[weather][f"avg_{metric}"] = np.mean(weather_performance[weather][metric])
                else:
                    weather_performance[weather][f"avg_{metric}"] = None
                    
        return weather_performance
        
    def _analyze_course_performance(self, perf_data: List[PerformanceData], usage_data: List[UsageRecord]) -> Dict:
        """コースごとのパフォーマンス分析"""
        course_performance = {}
        
        for perf in perf_data:
            # 同じ日付の使用記録を探す
            matching_usage = [u for u in usage_data if u.date.date() == perf.date.date()]
            if matching_usage:
                course = matching_usage[0].course
                if course not in course_performance:
                    course_performance[course] = {
                        "count": 0,
                        "carry_distance": [],
                        "total_distance": [],
                        "dispersion": []
                    }
                    
                course_performance[course]["count"] += 1
                course_performance[course]["carry_distance"].append(perf.carry_distance)
                course_performance[course]["total_distance"].append(perf.total_distance)
                course_performance[course]["dispersion"].append(perf.dispersion)
                
        # 各コースごとの平均値を計算
        for course in course_performance:
            for metric in ["carry_distance", "total_distance", "dispersion"]:
                if course_performance[course][metric]:
                    course_performance[course][f"avg_{metric}"] = np.mean(course_performance[course][metric])
                else:
                    course_performance[course][f"avg_{metric}"] = None
                    
        return course_performance
        
    def _interpret_correlation(self, correlation: float, trend: float) -> str:
        """相関係数とトレンドの解釈を生成"""
        if correlation is None or trend is None:
            return "データ不足のため分析できません"
            
        interpretation = []
        
        # 相関係数の解釈
        if abs(correlation) < 0.3:
            interpretation.append("使用回数との相関は弱いです")
        elif abs(correlation) < 0.7:
            interpretation.append("使用回数と中程度の相関があります")
        else:
            interpretation.append("使用回数と強い相関があります")
            
        # トレンドの解釈
        if abs(trend) < 0.1:
            interpretation.append("パフォーマンスは安定しています")
        elif trend > 0:
            interpretation.append("パフォーマンスは向上傾向にあります")
        else:
            interpretation.append("パフォーマンスは低下傾向にあります")
            
        return "。".join(interpretation)
        
    def _generate_correlation_recommendations(self, correlations: Dict, weather_correlations: Dict) -> List[str]:
        """相関分析に基づく推奨事項を生成"""
        recommendations = []
        
        # 使用回数との相関に基づく推奨
        for metric, data in correlations.items():
            if data["correlation"] is not None and abs(data["correlation"]) > 0.5:
                if data["correlation"] > 0:
                    recommendations.append(f"{metric}は使用回数が多いほど向上する傾向があります")
                else:
                    recommendations.append(f"{metric}は使用回数が多いほど低下する傾向があります")
                    
        # 天候との相関に基づく推奨
        for weather, data in weather_correlations.items():
            if data["count"] >= 5:  # 十分なデータがある場合のみ
                metrics = []
                for metric in ["carry_distance", "total_distance", "launch_angle", "spin_rate"]:
                    if data[f"avg_{metric}"] is not None:
                        metrics.append(f"{metric}: {data[f'avg_{metric}']:.1f}")
                if metrics:
                    recommendations.append(f"{weather}の条件下では: {', '.join(metrics)}")
                    
        return recommendations

class ClubSet:
    """ゴルフクラブセットを管理するクラス"""
    
    def __init__(self, name: str = "My Club Set"):
        self.name = name
        self.clubs: Dict[str, Club] = {}
        
    def add_club(self, club: Club) -> None:
        """クラブをセットに追加"""
        self.clubs[club.name] = club
        
    def remove_club(self, club_name: str) -> None:
        """クラブをセットから削除"""
        if club_name in self.clubs:
            del self.clubs[club_name]
            
    def get_club(self, club_name: str) -> Optional[Club]:
        """指定した名前のクラブを取得"""
        return self.clubs.get(club_name)
        
    def get_all_clubs(self) -> List[Club]:
        """セット内の全てのクラブを取得"""
        return list(self.clubs.values())
        
    def search_clubs(self, **kwargs) -> List[Club]:
        """条件に合致するクラブを検索"""
        results = []
        for club in self.clubs.values():
            match = True
            for key, value in kwargs.items():
                if hasattr(club, key):
                    if isinstance(value, (int, float)):
                        # 数値の場合は範囲検索
                        if isinstance(value, tuple) and len(value) == 2:
                            if not (value[0] <= getattr(club, key) <= value[1]):
                                match = False
                                break
                        else:
                            if getattr(club, key) != value:
                                match = False
                                break
                    else:
                        # 文字列の場合は部分一致
                        if value.lower() not in str(getattr(club, key)).lower():
                            match = False
                            break
                else:
                    match = False
                    break
            if match:
                results.append(club)
        return results
        
    def filter_by_manufacturer(self, manufacturer: str) -> List[Club]:
        """メーカーでフィルタリング"""
        return [club for club in self.clubs.values() 
                if manufacturer.lower() in club.manufacturer.lower()]
        
    def filter_by_loft_range(self, min_loft: float, max_loft: float) -> List[Club]:
        """ロフト角の範囲でフィルタリング"""
        return [club for club in self.clubs.values() 
                if min_loft <= club.loft <= max_loft]
        
    def filter_by_shaft_flex(self, shaft_flex: str) -> List[Club]:
        """シャフトの硬さでフィルタリング"""
        return [club for club in self.clubs.values() 
                if shaft_flex.lower() in club.shaft_flex.lower()]
        
    def compare_clubs(self, club1_name: str, club2_name: str) -> Dict:
        """2つのクラブを比較"""
        club1 = self.get_club(club1_name)
        club2 = self.get_club(club2_name)
        
        if not club1 or not club2:
            return {"error": "指定したクラブが見つかりません"}
            
        comparison = {
            "loft_difference": club1.loft - club2.loft,
            "length_difference": club1.length - club2.length,
            "weight_difference": club1.weight - club2.weight,
            "same_manufacturer": club1.manufacturer == club2.manufacturer,
            "same_shaft_flex": club1.shaft_flex == club2.shaft_flex,
            "same_head_material": club1.head_material == club2.head_material,
            "same_shaft_material": club1.shaft_material == club2.shaft_material,
            "same_grip_type": club1.grip_type == club2.grip_type
        }
        return comparison
        
    def analyze_set(self) -> Dict:
        """クラブセットの分析"""
        if not self.clubs:
            return {"error": "クラブセットが空です"}
            
        analysis = {
            "total_clubs": len(self.clubs),
            "manufacturers": {},
            "shaft_flexes": {},
            "head_materials": {},
            "shaft_materials": {},
            "grip_types": {},
            "loft_range": (float('inf'), float('-inf')),
            "length_range": (float('inf'), float('-inf')),
            "weight_range": (float('inf'), float('-inf')),
            "average_loft": 0,
            "average_length": 0,
            "average_weight": 0
        }
        
        total_loft = 0
        total_length = 0
        total_weight = 0
        
        for club in self.clubs.values():
            # メーカーの集計
            analysis["manufacturers"][club.manufacturer] = analysis["manufacturers"].get(club.manufacturer, 0) + 1
            
            # シャフトの硬さの集計
            analysis["shaft_flexes"][club.shaft_flex] = analysis["shaft_flexes"].get(club.shaft_flex, 0) + 1
            
            # ヘッド素材の集計
            analysis["head_materials"][club.head_material] = analysis["head_materials"].get(club.head_material, 0) + 1
            
            # シャフト素材の集計
            analysis["shaft_materials"][club.shaft_material] = analysis["shaft_materials"].get(club.shaft_material, 0) + 1
            
            # グリップタイプの集計
            analysis["grip_types"][club.grip_type] = analysis["grip_types"].get(club.grip_type, 0) + 1
            
            # ロフト角の範囲
            analysis["loft_range"] = (
                min(analysis["loft_range"][0], club.loft),
                max(analysis["loft_range"][1], club.loft)
            )
            
            # 長さの範囲
            analysis["length_range"] = (
                min(analysis["length_range"][0], club.length),
                max(analysis["length_range"][1], club.length)
            )
            
            # 重量の範囲
            analysis["weight_range"] = (
                min(analysis["weight_range"][0], club.weight),
                max(analysis["weight_range"][1], club.weight)
            )
            
            total_loft += club.loft
            total_length += club.length
            total_weight += club.weight
            
        # 平均値の計算
        analysis["average_loft"] = total_loft / len(self.clubs)
        analysis["average_length"] = total_length / len(self.clubs)
        analysis["average_weight"] = total_weight / len(self.clubs)
        
        return analysis
        
    def optimize_set(self, target_gaps: List[float] = None) -> Dict:
        """クラブセットの最適化"""
        if not self.clubs:
            return {"error": "クラブセットが空です"}
            
        # デフォルトのロフト角の間隔
        if target_gaps is None:
            target_gaps = [4.0]  # デフォルトは4度間隔
            
        # ロフト角でソート
        sorted_clubs = sorted(self.clubs.values(), key=lambda x: x.loft)
        
        # ロフト角の間隔を計算
        gaps = []
        for i in range(len(sorted_clubs) - 1):
            gap = sorted_clubs[i + 1].loft - sorted_clubs[i].loft
            gaps.append(gap)
            
        # 最適化の提案
        suggestions = {
            "current_gaps": gaps,
            "target_gaps": target_gaps,
            "recommendations": []
        }
        
        # 間隔が大きすぎる箇所を特定
        for i, gap in enumerate(gaps):
            if gap > max(target_gaps) * 1.2:  # 20%以上の超過
                suggestions["recommendations"].append({
                    "type": "gap_too_large",
                    "position": i,
                    "current_gap": gap,
                    "suggestion": f"{sorted_clubs[i].name}と{sorted_clubs[i+1].name}の間のロフト角の差が大きすぎます。"
                })
                
        # 間隔が小さすぎる箇所を特定
        for i, gap in enumerate(gaps):
            if gap < min(target_gaps) * 0.8:  # 20%以上の不足
                suggestions["recommendations"].append({
                    "type": "gap_too_small",
                    "position": i,
                    "current_gap": gap,
                    "suggestion": f"{sorted_clubs[i].name}と{sorted_clubs[i+1].name}の間のロフト角の差が小さすぎます。"
                })
                
        # シャフトの硬さの統一性チェック
        shaft_flexes = set(club.shaft_flex for club in self.clubs.values())
        if len(shaft_flexes) > 1:
            suggestions["recommendations"].append({
                "type": "shaft_flex_inconsistency",
                "current_flexes": list(shaft_flexes),
                "suggestion": "シャフトの硬さが統一されていません。"
            })
            
        # メーカーの統一性チェック
        manufacturers = set(club.manufacturer for club in self.clubs.values())
        if len(manufacturers) > 1:
            suggestions["recommendations"].append({
                "type": "manufacturer_inconsistency",
                "current_manufacturers": list(manufacturers),
                "suggestion": "メーカーが統一されていません。"
            })
            
        return suggestions
        
    def to_dict(self) -> Dict:
        """クラブセットの情報を辞書形式で返す"""
        return {
            "name": self.name,
            "clubs": {name: club.to_dict() for name, club in self.clubs.items()}
        }
        
    @classmethod
    def from_dict(cls, data: Dict) -> 'ClubSet':
        """辞書からクラブセットオブジェクトを作成"""
        club_set = cls(data["name"])
        for club_data in data["clubs"].values():
            club = Club.from_dict(club_data)
            club_set.add_club(club)
        return club_set
        
    def save_to_file(self, file_path: Union[str, Path]) -> None:
        """クラブセットの情報をJSONファイルに保存"""
        data = self.to_dict()
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    @classmethod
    def load_from_file(cls, file_path: Union[str, Path]) -> 'ClubSet':
        """JSONファイルからクラブセットを読み込み"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)
        
    def __str__(self) -> str:
        return f"{self.name} ({len(self.clubs)} clubs)"
        
    def __repr__(self) -> str:
        return f"ClubSet({self.name}, {len(self.clubs)} clubs)" 