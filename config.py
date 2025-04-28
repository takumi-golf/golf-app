import os
from dotenv import load_dotenv
from pathlib import Path

# .envファイルの読み込み
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# データベース設定
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:WecA4JagjpsziLi2_N9g@localhost:5432/golfclub')
SQL_ECHO = os.getenv('SQL_ECHO', 'False').lower() == 'true'

# アプリケーション設定
APP_NAME = os.getenv('APP_NAME', 'GolfClub')
APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# セキュリティ設定
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))

# メール設定
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
EMAIL_USERNAME = os.getenv('EMAIL_USERNAME', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')

# Slack設定
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN', '')
SLACK_CHANNEL_ID = os.getenv('SLACK_CHANNEL_ID', '')

# バックアップ設定
BACKUP_DIR = os.getenv('BACKUP_DIR', 'backups')
BACKUP_INTERVAL_HOURS = int(os.getenv('BACKUP_INTERVAL_HOURS', '24'))
MAX_BACKUP_FILES = int(os.getenv('MAX_BACKUP_FILES', '30'))

# ディレクトリの作成
Path(BACKUP_DIR).mkdir(exist_ok=True) 