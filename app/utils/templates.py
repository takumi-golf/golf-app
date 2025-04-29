from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.utils.analytics import GoogleAnalytics

class TemplateManager:
    """テンプレート管理クラス"""
    
    def __init__(self):
        self.templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))
        self.analytics = GoogleAnalytics()
        
    def get_templates(self):
        """テンプレートエンジンを取得"""
        return self.templates
        
    def get_analytics(self):
        """Analyticsインスタンスを取得"""
        return self.analytics
        
    def get_template_context(self, request, **kwargs):
        """テンプレートコンテキストを取得"""
        context = {
            "request": request,
            "analytics": self.analytics,
            **kwargs
        }
        return context 