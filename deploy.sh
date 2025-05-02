#!/bin/bash

# システムの更新
sudo apt update && sudo apt upgrade -y

# 必要なパッケージのインストール
sudo apt install -y python3-pip python3-venv nginx

# プロジェクトディレクトリの作成
mkdir -p ~/golf-recommend
cd ~/golf-recommend

# バックエンドのセットアップ
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# ログディレクトリの作成
mkdir -p logs

# systemdサービスの設定
sudo cp golf-recommend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable golf-recommend
sudo systemctl start golf-recommend

# Nginxの設定
sudo cp nginx/golf-recommend.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/golf-recommend.conf /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# フロントエンドのビルド
cd ../frontend
npm install
npm run build

# 権限の設定
sudo chown -R ubuntu:ubuntu ~/golf-recommend
sudo chmod -R 755 ~/golf-recommend

echo "デプロイが完了しました！" 