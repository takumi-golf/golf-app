# ゴルフクラブレコメンデーションシステム デプロイ手順

## 環境要件
- Ubuntu 22.04 LTS
- Node.js 20.x
- Python 3.10以上
- PostgreSQL 14以上

## デプロイ手順

### 1. システムの準備
```bash
# システムの更新
sudo apt-get update
sudo apt-get upgrade -y

# 必要なパッケージのインストール
sudo apt-get install -y python3-pip python3-venv postgresql postgresql-contrib
```

### 2. アプリケーションのデプロイ
```bash
# アプリケーションディレクトリの作成
mkdir -p /home/ubuntu/golf-app
cd /home/ubuntu/golf-app

# リポジトリのクローン
git clone <repository-url> .

# フロントエンドのセットアップ
cd frontend
npm install
npm run build

# バックエンドのセットアップ
cd ../backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. データベースのセットアップ
```bash
# PostgreSQLの設定
sudo -u postgres psql
CREATE DATABASE golf_recommend;
CREATE USER golf_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE golf_recommend TO golf_user;
\q

# データベースのマイグレーション
cd /home/ubuntu/golf-app/backend
python manage.py migrate
```

### 4. サービスの起動
```bash
# バックエンドサービスの起動
cd /home/ubuntu/golf-app/backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000

# フロントエンドサービスの起動
cd /home/ubuntu/golf-app/frontend
npm start
```

## トラブルシューティング

### 1. ポートの競合
```bash
# 使用中のポートを確認
sudo lsof -i :8000
sudo lsof -i :3000

# プロセスの終了
sudo kill -9 <PID>
```

### 2. データベース接続エラー
- PostgreSQLのステータス確認: `sudo systemctl status postgresql`
- ログの確認: `sudo tail -f /var/log/postgresql/postgresql-14-main.log`

### 3. アプリケーションログ
- バックエンドログ: `tail -f /home/ubuntu/golf-app/backend/logs/app.log`
- フロントエンドログ: `tail -f /home/ubuntu/golf-app/frontend/logs/app.log`

## 環境切り替え

### 開発環境
```bash
export NODE_ENV=development
export REACT_APP_API_URL=http://localhost:8000
```

### 本番環境
```bash
export NODE_ENV=production
export REACT_APP_API_URL=https://api.your-domain.com
```

## バックアップとリストア

### データベースのバックアップ
```bash
pg_dump -U golf_user golf_recommend > backup.sql
```

### データベースのリストア
```bash
psql -U golf_user golf_recommend < backup.sql
```

## セキュリティ設定

### 1. ファイアウォールの設定
```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 2. SSL/TLS証明書の設定
```bash
sudo certbot --nginx -d your-domain.com
```

## メンテナンス

### 1. ログローテーション
```bash
sudo logrotate -f /etc/logrotate.d/golf-app
```

### 2. ディスク容量の監視
```bash
df -h
du -h --max-depth=1 /home/ubuntu/golf-app
```

### 3. パフォーマンスモニタリング
```bash
htop
netstat -tulpn
``` 