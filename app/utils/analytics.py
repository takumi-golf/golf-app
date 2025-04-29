import logging
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv
import json

load_dotenv()

class GoogleAnalytics:
    """Google Analyticsのユーティリティクラス"""
    
    def __init__(self):
        self.tracking_id = os.getenv("GA_TRACKING_ID")
        self.measurement_id = os.getenv("GA_MEASUREMENT_ID")
        self.setup_logging()
        
    def setup_logging(self):
        """ロギングの設定"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/analytics.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def get_ga_script(self) -> str:
        """GA4のスクリプトを取得"""
        return f"""
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id={self.measurement_id}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{self.measurement_id}');
        </script>
        """
        
    def track_page_view(self, page_path: str, page_title: str, user_id: Optional[str] = None) -> str:
        """ページビューのトラッキング"""
        try:
            params = {
                'page_path': page_path,
                'page_title': page_title
            }
            if user_id:
                params['user_id'] = user_id
                
            script = f"""
            <script>
                gtag('event', 'page_view', {json.dumps(params)});
            </script>
            """
            self.logger.info(f"Page view tracked: {page_path} - {page_title}")
            return script
        except Exception as e:
            self.logger.error(f"Error tracking page view: {e}")
            return ""
            
    def track_event(self, event_name: str, event_params: Dict[str, Any], user_id: Optional[str] = None) -> str:
        """イベントのトラッキング"""
        try:
            if user_id:
                event_params['user_id'] = user_id
                
            script = f"""
            <script>
                gtag('event', '{event_name}', {json.dumps(event_params)});
            </script>
            """
            self.logger.info(f"Event tracked: {event_name} - {event_params}")
            return script
        except Exception as e:
            self.logger.error(f"Error tracking event: {e}")
            return ""
            
    def track_user_action(self, action_type: str, action_details: Dict[str, Any], user_id: Optional[str] = None) -> str:
        """ユーザーアクションのトラッキング"""
        try:
            params = {
                'action_type': action_type,
                **action_details
            }
            if user_id:
                params['user_id'] = user_id
                
            script = f"""
            <script>
                gtag('event', 'user_action', {json.dumps(params)});
            </script>
            """
            self.logger.info(f"User action tracked: {action_type} - {action_details}")
            return script
        except Exception as e:
            self.logger.error(f"Error tracking user action: {e}")
            return ""
            
    def track_error(self, error_type: str, error_message: str, user_id: Optional[str] = None) -> str:
        """エラーのトラッキング"""
        try:
            params = {
                'error_type': error_type,
                'error_message': error_message
            }
            if user_id:
                params['user_id'] = user_id
                
            script = f"""
            <script>
                gtag('event', 'error', {json.dumps(params)});
            </script>
            """
            self.logger.info(f"Error tracked: {error_type} - {error_message}")
            return script
        except Exception as e:
            self.logger.error(f"Error tracking error: {e}")
            return "" 