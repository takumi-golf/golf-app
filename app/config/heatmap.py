from typing import Dict, List
import os
from dotenv import load_dotenv

load_dotenv()

class HeatmapConfig:
    """Hotjarの設定クラス"""
    
    # Hotjar設定
    SITE_ID = os.getenv("HOTJAR_SITE_ID")
    SNIPPET_VERSION = os.getenv("HOTJAR_SNIPPET_VERSION")
    
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
    
    # トラッキング対象要素
    TRACKED_ELEMENTS: Dict[str, List[str]] = {
        "navigation": [
            "nav-menu",
            "search-bar",
            "user-menu"
        ],
        "club_listing": [
            "club-card",
            "filter-options",
            "sort-options"
        ],
        "club_detail": [
            "spec-table",
            "compare-button",
            "price-info"
        ],
        "user_forms": [
            "login-form",
            "register-form",
            "profile-form"
        ]
    }
    
    # フォームトラッキング設定
    FORM_TRACKING: Dict[str, Dict[str, str]] = {
        "login_form": {
            "form_id": "login-form",
            "track_fields": ["email", "password"]
        },
        "register_form": {
            "form_id": "register-form",
            "track_fields": ["email", "password", "name"]
        },
        "profile_form": {
            "form_id": "profile-form",
            "track_fields": ["name", "age", "handicap"]
        }
    }
    
    # ヒートマップ設定
    HEATMAP_SETTINGS: Dict[str, bool] = {
        "track_clicks": True,
        "track_moves": True,
        "track_scrolls": True,
        "track_form_interactions": True,
        "track_error_messages": True
    } 