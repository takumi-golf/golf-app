import os
from pathlib import Path
from dotenv import load_dotenv

# ベースディレクトリ
BASE_DIR = Path(__file__).resolve().parent

# .envファイルのパス
ENV_FILE = BASE_DIR / ".env"

# .envファイルが存在しない場合は作成
if not ENV_FILE.exists():
    try:
        with open(ENV_FILE, "w", encoding="utf-8") as f:
            f.write("""# データベース設定
DATABASE_URL=sqlite:///./golf_clubs.db

# Slack設定
SLACK_WEBHOOK_URL=your_slack_webhook_url_here

# スクレイピング設定
SCRAPING_TIMEOUT=30
MAX_RETRIES=3
RETRY_DELAY=2.0

# ログ設定
LOG_LEVEL=INFO

# デバッグ設定
DEBUG=True
""")
        print(f".envファイルを作成しました: {ENV_FILE}")
    except Exception as e:
        print(f".envファイルの作成に失敗しました: {str(e)}")

# .envファイルの読み込み
try:
    load_dotenv(dotenv_path=ENV_FILE, encoding="utf-8")
    print(".envファイルを読み込みました")
except Exception as e:
    print(f".envファイルの読み込みに失敗しました: {str(e)}")
    print("デフォルト設定を使用します。")

# データベース設定
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./golf_clubs.db")

# Slack設定
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

# スクレイピング設定
SCRAPING_TIMEOUT = int(os.getenv("SCRAPING_TIMEOUT", "30"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY = float(os.getenv("RETRY_DELAY", "2.0"))

# ログ設定
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "scraper.log"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# デバッグ設定
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# 出力ディレクトリ
OUTPUT_DIR = BASE_DIR / "output"
DATA_FILE = OUTPUT_DIR / "golf_data.json"

# データベース設定
SQL_ECHO = os.getenv("SQL_ECHO", "False").lower() == "true"
REDIS_URL = "redis://localhost:6379/0"

# セキュリティ設定
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# メール設定
MAIL_USERNAME = os.getenv("MAIL_USERNAME", "your-email@example.com")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "your-email-password")
MAIL_FROM = os.getenv("MAIL_FROM", "your-email@example.com")
MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
MAIL_TLS = os.getenv("MAIL_TLS", "True").lower() == "true"
MAIL_SSL = os.getenv("MAIL_SSL", "False").lower() == "true"