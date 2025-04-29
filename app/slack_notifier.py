import os
import json
import requests
from datetime import datetime
from typing import Dict, Any, Optional

class SlackNotifier:
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or os.getenv('SLACK_WEBHOOK_URL')
        if not self.webhook_url:
            raise ValueError("Slack webhook URLが設定されていません")

    def send_message(self, message: str, level: str = "info", details: Optional[Dict[str, Any]] = None):
        """Slackにメッセージを送信"""
        try:
            # メッセージの色を設定
            color_map = {
                "info": "#36a64f",  # 緑
                "warning": "#ffcc00",  # 黄
                "error": "#ff0000"  # 赤
            }
            color = color_map.get(level, "#36a64f")

            # メッセージの構造を作成
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{level.upper()}*: {message}"
                    }
                }
            ]

            # 詳細情報がある場合は追加
            if details:
                details_text = "```\n" + json.dumps(details, indent=2, ensure_ascii=False) + "\n```"
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": details_text
                    }
                })

            # タイムスタンプを追加
            blocks.append({
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"実行時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    }
                ]
            })

            # Slackに送信
            payload = {
                "attachments": [
                    {
                        "color": color,
                        "blocks": blocks
                    }
                ]
            }

            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()

        except Exception as e:
            print(f"Slack通知の送信に失敗しました: {str(e)}")

    def notify_scraping_start(self, target: str):
        """スクレイピング開始を通知"""
        self.send_message(
            f"スクレイピングを開始します: {target}",
            level="info"
        )

    def notify_scraping_complete(self, target: str, count: int):
        """スクレイピング完了を通知"""
        self.send_message(
            f"スクレイピングが完了しました: {target} ({count}件)",
            level="info"
        )

    def notify_error(self, error: Exception, context: Optional[Dict[str, Any]] = None):
        """エラーを通知"""
        details = {
            "error": str(error),
            "type": type(error).__name__
        }
        if context:
            details.update(context)
        
        self.send_message(
            "スクレイピング中にエラーが発生しました",
            level="error",
            details=details
        ) 