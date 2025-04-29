import streamlit as st
from typing import Dict, Any, Optional
import json
from app.config.heatmap import HeatmapConfig
import logging
import os
from dotenv import load_dotenv

load_dotenv()

class HeatmapTracker:
    """ヒートマップのトラッキングクラス"""
    
    def __init__(self):
        self.config = HeatmapConfig()
        
    def initialize_hotjar(self):
        """Hotjarの初期化"""
        st.markdown(f"""
        <script>
            (function(h,o,t,j,a,r){{
                h.hj=h.hj||function(){{(h.hj.q=h.hj.q||[]).push(arguments)}};
                h._hjSettings={{hjid:{self.config.HOTJAR_ID},hjsv:{self.config.HOTJAR_SNIPPET_VERSION}}};
                a=o.getElementsByTagName('head')[0];
                r=o.createElement('script');r.async=1;
                r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
                a.appendChild(r);
            }})(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
        </script>
        """, unsafe_allow_html=True)
        
    def track_page(self, page_path: str):
        """ページのトラッキング"""
        if page_path not in self.config.TRACKED_PAGES:
            return
            
        st.markdown(f"""
        <script>
            hj('trackPageview');
        </script>
        """, unsafe_allow_html=True)
        
    def track_element(self, element_name: str, element_data: Optional[Dict[str, Any]] = None):
        """要素のトラッキング"""
        if element_name not in self.config.TRACKED_ELEMENTS:
            return
            
        element = self.config.TRACKED_ELEMENTS[element_name]
        data = {
            'selector': element['selector'],
            'type': element['type']
        }
        
        if element_data:
            data.update(element_data)
            
        st.markdown(f"""
        <script>
            hj('trackElement', {json.dumps(data)});
        </script>
        """, unsafe_allow_html=True)
        
    def configure_heatmap(self):
        """ヒートマップの設定"""
        st.markdown(f"""
        <script>
            hj('configure', {json.dumps(self.config.HEATMAP_SETTINGS)});
        </script>
        """, unsafe_allow_html=True)

class HotjarTracker:
    """Hotjarのトラッキングクラス"""
    
    def __init__(self):
        self.site_id = os.getenv("HOTJAR_SITE_ID")
        self.snippet_version = os.getenv("HOTJAR_SNIPPET_VERSION")
        self.setup_logging()
        
    def setup_logging(self):
        """ロギングの設定"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/heatmap.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def get_hotjar_script(self) -> str:
        """Hotjarのスクリプトを取得"""
        return f"""
        <!-- Hotjar Tracking Code -->
        <script>
            (function(h,o,t,j,a,r){{
                h.hj=h.hj||function(){{(h.hj.q=h.hj.q||[]).push(arguments)}};
                h._hjSettings={{hjid:{self.site_id},hjsv:{self.snippet_version}}};
                a=o.getElementsByTagName('head')[0];
                r=o.createElement('script');r.async=1;
                r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
                a.appendChild(r);
            }})(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
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
                hj('trackPageview', {json.dumps(params)});
            </script>
            """
            self.logger.info(f"Page view tracked: {page_path} - {page_title}")
            return script
        except Exception as e:
            self.logger.error(f"Error tracking page view: {e}")
            return ""
            
    def track_user_interaction(self, element_id: str, interaction_type: str, user_id: Optional[str] = None) -> str:
        """ユーザーインタラクションのトラッキング"""
        try:
            params = {
                'element_id': element_id,
                'interaction_type': interaction_type
            }
            if user_id:
                params['user_id'] = user_id
                
            script = f"""
            <script>
                hj('trackInteraction', {json.dumps(params)});
            </script>
            """
            self.logger.info(f"User interaction tracked: {element_id} - {interaction_type}")
            return script
        except Exception as e:
            self.logger.error(f"Error tracking user interaction: {e}")
            return ""
            
    def track_form_submission(self, form_id: str, form_data: Dict[str, Any], user_id: Optional[str] = None) -> str:
        """フォーム送信のトラッキング"""
        try:
            params = {
                'form_id': form_id,
                'form_data': form_data
            }
            if user_id:
                params['user_id'] = user_id
                
            script = f"""
            <script>
                hj('trackFormSubmission', {json.dumps(params)});
            </script>
            """
            self.logger.info(f"Form submission tracked: {form_id} - {form_data}")
            return script
        except Exception as e:
            self.logger.error(f"Error tracking form submission: {e}")
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
                hj('trackError', {json.dumps(params)});
            </script>
            """
            self.logger.info(f"Error tracked: {error_type} - {error_message}")
            return script
        except Exception as e:
            self.logger.error(f"Error tracking error: {e}")
            return "" 