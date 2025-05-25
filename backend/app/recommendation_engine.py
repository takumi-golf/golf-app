import numpy as np
import pandas as pd
from surprise import Dataset, Reader, SVD
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from .models.player import PlayerProfile, ClubSpecification, Brand, ClubModel, Shaft, Recommendation
from .schemas.recommendation import RecommendationRequest
from .core.error_handlers import (
    HeadSpeedError, HandicapError, AgeError, GenderError,
    ErrorMessages
)

class GolfClubRecommender:
    """ゴルフクラブ推奨エンジン"""
    def __init__(self, db: Session):
        self.db = db
        self.model = None  # 初期状態ではモデルは未トレーニング
    
    def _train_model(self):
        """協調フィルタリングモデルのトレーニング"""
        # TODO: 実際のデータが利用可能になったら実装
        pass
    
    def analyze_player(self, profile: PlayerProfile) -> tuple[str, str]:
        """プレイヤーのプロファイルを分析してセグメントと推奨シャフトを決定"""
        # ヘッドスピードに基づくセグメント分類
        segment = self._determine_segment(profile.head_speed)
        
        # シャフト推奨
        shaft_recommendation = self.recommend_shaft({
            "head_speed": profile.head_speed,
            "handicap": profile.handicap,
            "age": profile.age,
            "gender": profile.gender
        })
        
        return segment, shaft_recommendation

    def _validate_input(self, profile: Dict[str, Any]) -> None:
        """入力値のバリデーション"""
        # ヘッドスピードのバリデーション
        if profile["head_speed"] <= 0 or profile["head_speed"] > 80.0:
            raise HeadSpeedError(ErrorMessages.HEAD_SPEED_INVALID)
        
        # ハンディキャップのバリデーション
        if profile["handicap"] < 0 or profile["handicap"] > 54.0:
            raise HandicapError(ErrorMessages.HANDICAP_INVALID)
        
        # 年齢のバリデーション
        if profile["age"] <= 0 or profile["age"] > 120:
            raise AgeError(ErrorMessages.AGE_INVALID)
        
        # 性別のバリデーション
        if profile["gender"].lower() not in ["male", "female"]:
            raise GenderError(ErrorMessages.GENDER_INVALID)

    def _determine_segment(self, head_speed: float) -> str:
        """ヘッドスピードに基づくセグメント判定"""
        if head_speed >= 45.0:
            return "high"
        elif head_speed >= 40.0:
            return "intermediate"
        else:
            return "low"

    def _get_shaft_flex(self, head_speed: float) -> str:
        """ヘッドスピードに基づくシャフトフレックス推奨"""
        if head_speed >= 46.0:
            return "X"
        elif head_speed >= 43.0:
            return "S"
        elif head_speed >= 40.0:
            return "R"
        elif head_speed >= 35.0:
            return "SR"
        else:
            return "L"

    def recommend_shaft(self, profile: Dict[str, Any]) -> str:
        """シャフト推奨"""
        flex = self._get_shaft_flex(profile["head_speed"])
        shaft_type = "スチール" if profile["head_speed"] >= 40.0 else "カーボン"
        return f"フレックス: {flex}, シャフト: {shaft_type}"

    def get_recommended_clubs(self, profile: PlayerProfile) -> list[ClubSpecification]:
        """プレイヤープロファイルに基づく推奨クラブの取得"""
        segment = self._determine_segment(profile.head_speed)
        
        # セグメントに基づくクラブの検索
        clubs = self.db.query(ClubSpecification)\
            .join(ClubModel)\
            .join(Brand)\
            .filter(ClubModel.category == segment)\
            .all()
        
        return clubs
    
    def _get_player_segment(self, head_speed: float, handicap: float, age: int, gender: str) -> str:
        """プレイヤーのセグメント判定"""
        segments = []
        
        # ヘッドスピードによる判定
        if head_speed >= 45.0:
            segments.append("high")
        elif head_speed >= 40.0:
            segments.append("intermediate")
        else:
            segments.append("low")
        
        # ハンディキャップによる判定
        if handicap <= 10.0:
            segments.append("expert")
        elif handicap <= 20.0:
            segments.append("intermediate")
        else:
            segments.append("beginner")
        
        # 年齢による判定
        if age < 20:
            segments.append("junior")
        elif age < 50:
            segments.append("adult")
        else:
            segments.append("senior")
        
        # 性別による判定
        segments.append(gender.lower())
        
        return "_".join(segments)
    
    def recommend_clubs(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """クラブの推奨"""
        # 入力値のバリデーション
        self._validate_input(profile)

        # プレイヤーセグメントの判定
        segment = self._get_player_segment(
            profile["head_speed"],
            profile["handicap"],
            profile["age"],
            profile["gender"]
        )

        # シャフトの推奨
        shaft_flex = self._get_shaft_flex(profile["head_speed"])
        shaft_recommendation = f"フレックス: {shaft_flex}, "
        shaft_recommendation += "シャフト: カーボン" if profile["head_speed"] < 40.0 else "シャフト: スチール"

        # 推奨クラブの取得
        recommended_clubs = self._get_clubs_by_segment(segment, shaft_flex)

        return {
            "segment": segment,
            "shaft_recommendation": shaft_recommendation,
            "recommended_clubs": recommended_clubs
        }
    
    def _get_clubs_by_segment(self, segment: str, shaft_flex: str) -> List[Dict[str, Any]]:
        """セグメントに基づくクラブセット推奨"""
        # セグメントごとのクラブ構成パターン
        segment_patterns = {
            "high_expert_adult_male": {
                "driver": {"loft_range": [8.5, 10.5]},
                "irons": {"start_number": 3, "end_number": 9},
                "wedges": [{"type": "PW"}, {"type": "SW"}, {"type": "LW"}]
            },
            # デフォルトパターン
            "default": {
                "driver": {"loft_range": [10.5, 12.0]},
                "irons": {"start_number": 5, "end_number": 9},
                "wedges": [{"type": "PW"}, {"type": "SW"}]
            }
        }
        
        # セグメントに基づくパターン選択
        pattern = segment_patterns.get(segment, segment_patterns["default"])
        recommended_clubs = []
        
        # ドライバーの推奨
        driver_specs = self.db.query(ClubSpecification).join(
            Shaft
        ).filter(
            ClubSpecification.club_type == "driver",
            ClubSpecification.loft.between(*pattern["driver"]["loft_range"]),
            Shaft.flex == shaft_flex
        ).first()
        
        if driver_specs:
            recommended_clubs.append({
                "club_type": "driver",
                "specifications": {
                    "brand": driver_specs.club_model.brand.name,
                    "model": driver_specs.club_model.name,
                    "club_type": driver_specs.club_type,
                    "loft": driver_specs.loft,
                    "lie_angle": driver_specs.lie_angle,
                    "length": driver_specs.length,
                    "shaft": driver_specs.shaft.model if driver_specs.shaft else None,
                    "flex": driver_specs.shaft.flex if driver_specs.shaft else None
                }
            })
        
        # アイアンセットの推奨
        for i in range(pattern["irons"]["start_number"], pattern["irons"]["end_number"] + 1):
            iron_specs = self.db.query(ClubSpecification).join(
                Shaft
            ).filter(
                ClubSpecification.club_type == f"{i}i",
                Shaft.flex == shaft_flex
            ).first()
            
            if iron_specs:
                recommended_clubs.append({
                    "club_type": f"{i}i",
                    "specifications": {
                        "brand": iron_specs.club_model.brand.name,
                        "model": iron_specs.club_model.name,
                        "club_type": iron_specs.club_type,
                        "loft": iron_specs.loft,
                        "lie_angle": iron_specs.lie_angle,
                        "length": iron_specs.length,
                        "shaft": iron_specs.shaft.model if iron_specs.shaft else None,
                        "flex": iron_specs.shaft.flex if iron_specs.shaft else None
                    }
                })
        
        # ウェッジの推奨
        for wedge in pattern["wedges"]:
            wedge_specs = self.db.query(ClubSpecification).join(
                Shaft
            ).filter(
                ClubSpecification.club_type == wedge["type"],
                Shaft.flex == shaft_flex
            ).first()
            
            if wedge_specs:
                recommended_clubs.append({
                    "club_type": wedge["type"],
                    "specifications": {
                        "brand": wedge_specs.club_model.brand.name,
                        "model": wedge_specs.club_model.name,
                        "club_type": wedge_specs.club_type,
                        "loft": wedge_specs.loft,
                        "lie_angle": wedge_specs.lie_angle,
                        "length": wedge_specs.length,
                        "shaft": wedge_specs.shaft.model if wedge_specs.shaft else None,
                        "flex": wedge_specs.shaft.flex if wedge_specs.shaft else None
                    }
                })
        
        return recommended_clubs 