import requests
from typing import Dict, Any, Optional
from app.config.ga4 import get_ga4_config

class GA4Tracker:
    def __init__(self):
        self.config = get_ga4_config()
        self.base_url = f"https://www.google-analytics.com/mp/collect"
        self.client_id = None

    def _send_event(self, event_name: str, params: Dict[str, Any]) -> bool:
        """イベントをGA4に送信"""
        try:
            url = f"{self.base_url}?measurement_id={self.config.measurement_id}&api_secret={self.config.api_secret}&stream_id={self.config.stream_id}"
            
            payload = {
                "client_id": self.client_id,
                "events": [{
                    "name": event_name,
                    "params": params
                }]
            }
            
            response = requests.post(url, json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"GA4 event sending failed: {e}")
            return False

    def track_page_view(self, page_path: str, page_title: str) -> bool:
        """ページビューをトラッキング"""
        return self._send_event("page_view", {
            "page_path": page_path,
            "page_title": page_title
        })

    def track_club_search(self, search_term: str, results_count: int) -> bool:
        """クラブ検索をトラッキング"""
        return self._send_event("club_search", {
            "search_term": search_term,
            "results_count": results_count
        })

    def track_club_view(self, club_id: str, club_name: str) -> bool:
        """クラブ詳細ページの閲覧をトラッキング"""
        return self._send_event("club_view", {
            "club_id": club_id,
            "club_name": club_name
        })

    def track_user_action(self, action_type: str, action_details: Dict[str, Any]) -> bool:
        """ユーザーアクションをトラッキング"""
        return self._send_event("user_action", {
            "action_type": action_type,
            **action_details
        }) 