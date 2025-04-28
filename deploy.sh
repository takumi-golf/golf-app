#!/bin/bash

# アプリケーションのディレクトリに移動
cd /home/ec2-user/golf-app

# 最新のコードを取得
git pull origin main

# 仮想環境の作成（初回のみ）
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 仮想環境をアクティベート
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt

# 環境変数の設定
export DATABASE_URL="postgresql://username:password@localhost:5432/golf_db"
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"

# アプリケーションの再起動
sudo systemctl restart golf-app 