from typing import Dict, List
import os
from dotenv import load_dotenv

load_dotenv()

class AnalyticsConfig:
    """Google Analyticsの設定クラス"""
    
    # トラッキングID
    GA_TRACKING_ID = os.getenv("GA_TRACKING_ID")
    GA_MEASUREMENT_ID = os.getenv("GA_MEASUREMENT_ID")
    
    # イベント定義
    EVENTS: Dict[str, Dict[str, str]] = {
        "page_view": {
            "category": "Page",
            "action": "View",
            "label": "Page View"
        },
        "user_login": {
            "category": "User",
            "action": "Login",
            "label": "User Login"
        },
        "user_logout": {
            "category": "User",
            "action": "Logout",
            "label": "User Logout"
        },
        "club_search": {
            "category": "Club",
            "action": "Search",
            "label": "Club Search"
        },
        "club_view": {
            "category": "Club",
            "action": "View",
            "label": "Club View"
        },
        "club_compare": {
            "category": "Club",
            "action": "Compare",
            "label": "Club Compare"
        }
    }
    
    # カスタムディメンション
    CUSTOM_DIMENSIONS: Dict[str, int] = {
        "user_type": 1,
        "club_category": 2,
        "manufacturer": 3,
        "price_range": 4
    }
    
    # カスタムメトリクス
    CUSTOM_METRICS: Dict[str, int] = {
        "session_duration": 1,
        "search_count": 2,
        "compare_count": 3,
        "view_count": 4
    }
    
    # トラッキング対象ページ
    TRACKED_PAGES: List[str] = [
        "/",
        "/clubs",
        "/clubs/search",
        "/clubs/compare",
        "/users/login",
        "/users/register",
        "/users/profile"
    ] 