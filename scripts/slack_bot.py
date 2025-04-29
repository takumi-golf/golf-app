from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import json
import os
import subprocess
from typing import Dict, List
import re

# ボットの初期化
app = App(token="xoxb-8817680417938-8830977427057-GZOYZNYITcVTWchZZmU6cQpu")

# ゴルフクラブのデータを読み込む
def load_club_data() -> Dict:
    try:
        with open('golf_clubs.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# クラブタイプのリスト
CLUB_TYPES = ["ドライバー", "フェアウェイウッド", "アイアン", "ウェッジ", "パター"]

# 開発支援コマンドの定義
DEVELOPMENT_COMMANDS = {
    "task": "抽象的な指示を具体的なタスクに分解します。例: `task ユーザー認証機能を追加して`",
    "help": "利用可能なコマンドを表示します"
}

# タスク分解の例
TASK_TEMPLATES = {
    "認証": [
        "ユーザーモデルの作成",
        "ログインAPIの実装",
        "パスワードハッシュ化の実装",
        "セッション管理の実装",
        "認証ミドルウェアの作成"
    ],
    "データベース": [
        "データベーススキーマの設計",
        "マイグレーションファイルの作成",
        "モデルの実装",
        "リレーションの設定",
        "インデックスの追加"
    ],
    "API": [
        "エンドポイントの設計",
        "リクエスト/レスポンススキーマの定義",
        "コントローラーの実装",
        "バリデーションの追加",
        "エラーハンドリングの実装"
    ]
}

# ヘルプメッセージの定義
def get_help_message():
    help_text = """
開発支援コマンド:
"""
    for cmd, desc in DEVELOPMENT_COMMANDS.items():
        help_text += f"- `{cmd}`: {desc}\n"
    return help_text

# 抽象的な指示を具体的なタスクに分解する関数
def break_down_task(instruction: str) -> List[str]:
    tasks = []
    
    # 認証関連のタスク
    if any(keyword in instruction for keyword in ["認証", "ログイン", "ログアウト", "サインイン", "サインアップ"]):
        tasks.extend(TASK_TEMPLATES["認証"])
    
    # データベース関連のタスク
    if any(keyword in instruction for keyword in ["データベース", "DB", "テーブル", "スキーマ"]):
        tasks.extend(TASK_TEMPLATES["データベース"])
    
    # API関連のタスク
    if any(keyword in instruction for keyword in ["API", "エンドポイント", "リクエスト", "レスポンス"]):
        tasks.extend(TASK_TEMPLATES["API"])
    
    # タスクが見つからない場合のデフォルト
    if not tasks:
        tasks = [
            "要件の分析",
            "設計書の作成",
            "実装計画の策定",
            "コードの実装",
            "テストの作成",
            "ドキュメントの作成"
        ]
    
    return tasks

# メッセージを処理する関数
def process_message(text: str, user: str, say):
    print(f"Processing message: {text} from user: {user}")
    text = text.lower()
    
    # タスク分解コマンド
    if text.startswith("task "):
        instruction = text[5:].strip()
        if instruction:
            tasks = break_down_task(instruction)
            response = f"<@{user}> 以下のタスクに分解しました:\n\n"
            for i, task in enumerate(tasks, 1):
                response += f"{i}. {task}\n"
            say(response)
        else:
            say(f"<@{user}> 指示を指定してください。例: `task ユーザー認証機能を追加して`")
    
    # ヘルプコマンド
    elif text == "help":
        say(get_help_message())
    
    else:
        say(f"<@{user}> 申し訳ありませんが、そのコマンドは理解できませんでした。`help`と入力して利用可能なコマンドを確認してください。")

# 通常のメッセージの処理
@app.message(".*")
def handle_message(message, say):
    print(f"Received message: {message}")
    text = message.get('text', '')
    user = message.get('user', '')
    process_message(text, user, say)

# ボットへのメンションに対する処理
@app.event("app_mention")
def handle_mention(event, say):
    print(f"Received mention event: {event}")
    text = event.get('text', '')
    user = event.get('user', '')
    
    message_text = ' '.join(text.split()[1:])
    print(f"Processed message text: {message_text}")
    
    if message_text:
        process_message(message_text, user, say)
    else:
        say(f"<@{user}> こんにちは！開発支援ボットです。`help`と入力して利用可能なコマンドを確認してください。")

# アプリの起動時の処理
@app.event("app_home_opened")
def handle_app_home_opened(event, say):
    print(f"App home opened: {event}")  # デバッグ用
    user = event.get('user', '')
    say(f"<@{user}> こんにちは！ゴルフクラブの情報をお探しですか？`help`と入力して利用可能なコマンドを確認してください。")

if __name__ == "__main__":
    print("Starting development support bot...")
    handler = SocketModeHandler(app=app, app_token="xapp-1-A08Q5ABELMQ-8841288169776-5e1aa8f345006bd5c499ad77413f51d0c532034317acf865f2c57428ff4eba87")
    handler.start() 