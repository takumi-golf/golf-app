# EC2デプロイ手順

## 1. ドメインの設定

### ドメインの取得
1. ドメイン登録サービスでドメインを購入
   - 例：お名前.com、Route 53
   - 使用ドメイン：`golf-ai.jp`

### DNSの設定
1. お名前.comでの設定
   - Aレコードの追加
     - ホスト名: @
     - 値: [EC2のElastic IPアドレス]
   - CNAMEレコードの追加
     - ホスト名: www
     - 値: @

2. その他のDNSプロバイダーを使用する場合
   - ネームサーバー情報を設定
   - AレコードでEC2のIPアドレスを指定

## 2. EC2の設定

### セキュリティグループ
```bash
# 必要なポートを開放
- HTTP (80)
- HTTPS (443)
- SSH (22)
```

### Elastic IPの割り当て
1. EC2コンソールでElastic IPを取得
2. インスタンスに割り当て

## 3. サーバー環境のセットアップ

### 必要なパッケージのインストール
```bash
sudo apt-get update
sudo apt-get install -y nginx python3-pip python3-venv certbot python3-certbot-nginx
```

### Nginxの設定
1. 設定ファイルの配置
```bash
sudo cp app/config/nginx.conf /etc/nginx/sites-available/golf-fitting
sudo ln -s /etc/nginx/sites-available/golf-fitting /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL証明書の取得
```bash
sudo certbot --nginx -d golf-ai.jp -d www.golf-ai.jp
```

## 4. アプリケーションのデプロイ

### 環境のセットアップ
```bash
# 仮想環境の作成
python3 -m venv venv
source venv/bin/activate

# 依存パッケージのインストール
pip install -r requirements.txt
```

### 環境変数の設定
```bash
# .envファイルの作成
cp .env.example .env
# 環境変数の編集
nano .env
```

### アプリケーションの起動
```bash
# Streamlitの起動
streamlit run app.py --server.port=8501
```

## 5. システムサービスの設定

### systemdサービスの作成
```bash
sudo nano /etc/systemd/system/golf-fitting.service
```

```ini
[Unit]
Description=Golf Fitting App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/your/app
Environment="PATH=/path/to/your/venv/bin"
ExecStart=/path/to/your/venv/bin/streamlit run app.py --server.port=8501
Restart=always

[Install]
WantedBy=multi-user.target
```

### サービスの起動
```bash
sudo systemctl daemon-reload
sudo systemctl start golf-fitting
sudo systemctl enable golf-fitting
```

## 6. メンテナンス

### ログの確認
```bash
# アプリケーションログ
journalctl -u golf-fitting -f

# Nginxログ
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### バックアップ
```bash
# データベースのバックアップ
python scripts/backup_database.py

# 設定ファイルのバックアップ
tar -czf config_backup.tar.gz .env app/config/
```

## 7. トラブルシューティング

### よくある問題と解決方法

1. アプリケーションが起動しない
   - ログを確認: `journalctl -u golf-fitting -f`
   - ポートが使用中でないか確認: `netstat -tulpn | grep 8501`

2. SSL証明書の更新
   - 自動更新の確認: `sudo certbot renew --dry-run`
   - 手動更新: `sudo certbot renew`

3. パフォーマンスの問題
   - リソース使用状況の確認: `top`, `htop`
   - Nginxの設定最適化 