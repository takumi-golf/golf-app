# SwingFit Pro - AIゴルフクラブレコメンデーションシステム

## 概要
SwingFit Proは、ユーザーのスイングデータやプレースタイル、身体的特徴に基づき、最適なゴルフクラブセット（14本）をAIが自動で提案するWebアプリケーションです。国内外のプロ・アマチュアのクラブセッティングデータや最新のゴルフ理論をもとに、ユーザー属性ごとに最適なクラブ構成を選定します。

## 特徴
- ユーザー属性（ヘッドスピード・ハンディキャップ・年齢・性別）ごとに最適な14本セットを自動生成
- 国内外のプロ・アマチュアのデータをもとにした10パターンのクラブセッティング
- クラブ種別・ブランド・モデル・ロフト・シャフト・フレックスなど詳細なスペックを提案
- セット詳細画面ではブランドごとのロゴ画像や色分けで視覚的に分かりやすく表示
- UI/UXは30〜50代ゴルファー向けに最適化
- CORSやAPIエンドポイントの柔軟な設定

## 技術スタック
- フロントエンド: React, Material-UI, Axios, React Router DOM
- バックエンド: FastAPI, Pydantic
- その他: ブランドロゴ画像（SVG/PNG）

## セキュリティ設定と環境変数の管理

### 環境変数の配置場所
環境変数ファイルは以下の場所に配置します：
```
C:\Users\[ユーザー名]\AppData\Local\golf-app\
├── env                  # 現在の環境設定
├── env.development      # 開発環境用
├── env.example          # テンプレート
└── env.production       # 本番環境用
```

### 環境変数の内容
各環境変数ファイルには以下の情報が含まれます：

```env
# データベース設定
DATABASE_URL=postgresql://user:password@localhost:5432/golfclub

# Slack設定
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...

# API設定
REACT_APP_API_BASE_URL=http://localhost:8000

# AWS設定
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_DEFAULT_REGION=ap-northeast-1
```

### 認証情報のローテーション
認証情報は定期的にローテーションする必要があります。以下のスクリプトを使用して自動化できます：

```powershell
# 認証情報のローテーション
.\scripts\rotate-credentials.ps1 -Environment development -Service all
```

ローテーションの頻度：
- AWS認証情報: 90日ごと
- Slackトークン: 180日ごと
- データベースパスワード: 90日ごと

### セキュリティチェック
定期的なセキュリティチェックを実施します：

```powershell
# セキュリティチェックの実行
.\scripts\security-check.ps1
```

チェック項目：
1. 環境変数ファイルの権限設定
2. 認証情報の有効期限
3. アクセスログの確認
4. セキュリティアップデートの確認

### 環境変数の切り替え
環境に応じて適切な環境変数ファイルを使用します：

```powershell
# 開発環境
copy env.development env

# 本番環境
copy env.production env
```

## セットアップ手順
### 1. バックエンド
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # (Windows)
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2. フロントエンド
```bash
cd frontend
npm install
npm start
```

### 3. ブランドロゴ画像の配置
`frontend/public/brand-logos/` ディレクトリを作成し、主要ブランドのSVG/PNGロゴ（例: `titleist.svg`, `taylormade.svg`, `callaway.svg` など）を配置してください。

## 画面構成
- トップ画面：ユーザー情報入力フォーム＋おすすめクラブセット一覧（簡易表示）
- セット詳細画面：14本すべてのクラブをブランドロゴ・色分け・スペック付きでリッチに表示

## APIエンドポイント
- `POST /api/recommendations/` : レコメンデーション生成
- `GET /api/recommendations/history/` : 履歴取得
- `POST /api/recommendations/{id}/feedback/` : フィードバック送信

## カスタマイズ例
- ブランドロゴ画像の追加・差し替え
- 推薦ロジックのパターン追加や重み調整
- UIテーマやレイアウトの変更

## 今後の拡張例
- クラブ比較・お気に入り登録機能
- PDF/印刷用レイアウト
- より詳細なマッチングスコアやフィードバック分析

## 注意事項
- 本システムは開発・検証用途です。実際のクラブ購入時は必ずフィッティングや試打を推奨します。
- CORS設定やAPIエンドポイントは運用環境に合わせて調整してください。
- 認証情報は定期的にローテーションし、セキュリティを維持してください。
- 環境変数ファイルはGitにコミットしないでください。

## トラブルシューティング
1. データベース接続エラー
   - 環境変数の設定を確認
   - データベースサービスの状態を確認

2. アプリケーション起動エラー
   - ログの確認: `journalctl -u golf-recommendation`
   - ポートの使用状況確認: `netstat -tulpn | grep 8000`

3. パフォーマンス問題
   - データベースのインデックス確認
   - クエリの最適化
   - キャッシュの活用

4. セキュリティ関連
   - 認証情報の有効期限確認
   - アクセスログの確認
   - セキュリティアップデートの適用

## 環境切り替え最適化ガイド

### 現状の主な問題点
1. フロントエンドのビルド時に毎回 `node_modules` を削除・再インストールしている
2. ビルド時間が5-10分と長い
3. パーミッション問題が頻発している
4. 環境切り替えが手動で複雑

### 短期的解決策：ビルドプロセスの最適化

#### 1. node_modules キャッシュの活用
```bash
#!/bin/bash
# improved-deploy.sh

FRONTEND_DIR="/home/ubuntu/golf-app/frontend"
BACKEND_DIR="/home/ubuntu/golf-app/backend"
ENV=${1:-"prod"}  # デフォルトは本番環境

# フロントエンドのビルド
cd $FRONTEND_DIR

# package-lock.json が変更された場合のみ node_modules を再インストール
if [ -f .package-lock-checksum ] && [ "$(md5sum package-lock.json | cut -d ' ' -f 1)" = "$(cat .package-lock-checksum)" ]; then
    echo "依存関係に変更なし - インストールをスキップします"
else
    echo "依存関係が変更されました - パッケージをインストールします"
    npm ci  # npm install より高速で信頼性が高い
    md5sum package-lock.json | cut -d ' ' -f 1 > .package-lock-checksum
fi

# 環境変数を設定してビルド
echo "Building for ${ENV} environment..."
export REACT_APP_ENV=$ENV
npm run build

# パーミッション設定
sudo chown -R www-data:www-data build/
sudo chmod -R 755 build/

# バックエンドの再起動
cd $BACKEND_DIR
sudo systemctl restart golf-app

echo "デプロイが完了しました！"
```

#### 2. direnv を使用した環境変数の自動切り替え
```bash
# インストール
sudo apt-get install direnv

# ~/.bashrc に追加
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
source ~/.bashrc

# プロジェクトディレクトリに .envrc ファイルを作成
cd /home/ubuntu/golf-app
cat > .envrc << EOF
export REACT_APP_ENV=\${REACT_APP_ENV:-production}
export NODE_ENV=\${NODE_ENV:-production}
EOF
```

### 長期的解決策：Dockerコンテナ化

#### フロントエンドの Dockerfile
```dockerfile
# ビルドステージ
FROM node:16-alpine AS builder

WORKDIR /app

# 依存関係をインストール（レイヤーキャッシュを活用）
COPY package.json package-lock.json ./
RUN npm ci

# ソースコードをコピーしてビルド
COPY . .
ARG REACT_APP_ENV=production
ENV REACT_APP_ENV=${REACT_APP_ENV}
RUN npm run build

# 本番ステージ
FROM nginx:alpine AS production
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose 設定
```yaml
# docker-compose.yml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      args:
        - REACT_APP_ENV=${APP_ENV:-production}
    ports:
      - "80:80"
    depends_on:
      - backend

  backend:
    build: ./backend
    environment:
      - NODE_ENV=${APP_ENV:-production}
    ports:
      - "3000:3000"
```

### 推奨される実装順序

1. 短期的解決策のスクリプトを実装
   - `improved-deploy.sh` の実装
   - direnv の設定

2. 環境変数管理の最適化
   - 環境別の設定ファイル作成
   - direnv の設定完了

3. CI/CDパイプラインの構築
   - GitHub Actions の設定
   - 自動テストの実装
   - 自動デプロイの設定

4. Dockerコンテナ化
   - Dockerfile の作成
   - Docker Compose の設定
   - コンテナ化のテスト

### 期待される効果

1. ビルド時間の短縮
   - 現在の5-10分から1-2分程度に短縮
   - キャッシュの活用による効率化

2. 運用効率の向上
   - 手動操作の削減
   - エラーの発生リスク低減
   - 環境切り替えの簡素化

3. 安定性の向上
   - パーミッション問題の解消
   - 環境の一貫性確保
   - デプロイの信頼性向上

---
ご質問・ご要望はいつでもお知らせください！ 

## 環境設定

### 必要な環境変数
`.env`ファイルを作成し、以下の環境変数を設定してください：

```env
# データベース設定
DATABASE_URL=sqlite:///./golf_recommendation.db  # 開発環境
# DATABASE_URL=postgresql://user:password@localhost:5432/golf_recommendation  # 本番環境

# 環境設定
ENV=development  # development, testing, production

# API設定
API_HOST=127.0.0.1
API_PORT=8000

# CORS設定
ALLOWED_ORIGINS=http://localhost:3000

# セキュリティ設定
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 開発環境のセットアップ

1. バックエンドのセットアップ
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. データベースの初期化
```bash
# 開発環境
python -c "from app.database.database import Base, engine; Base.metadata.create_all(bind=engine)"

# 本番環境
alembic upgrade head
```

3. テストデータの投入
```bash
python scripts/seed_data.py
```

## デプロイ手順

### 開発環境
1. ローカルでの開発
```bash
cd backend
uvicorn main:app --reload
```

2. テストの実行
```bash
pytest
```

### 本番環境（EC2）
1. EC2インスタンスへの接続
```bash
ssh -i your-key.pem ec2-user@your-instance-ip
```

2. アプリケーションの更新
```bash
cd /path/to/application
git pull origin main
```

3. 依存関係の更新
```bash
cd backend
pip install -r requirements.txt
```

4. データベースのマイグレーション
```bash
alembic upgrade head
```

5. アプリケーションの再起動
```bash
sudo systemctl restart golf-recommendation
```

## 環境の切り替え

### 開発環境
- データベース: SQLite
- ホスト: localhost
- ポート: 8000

### テスト環境
- データベース: PostgreSQL（テスト用）
- ホスト: test-server
- ポート: 8000

### 本番環境
- データベース: PostgreSQL
- ホスト: EC2インスタンス
- ポート: 80/443

## 注意事項
1. 本番環境の認証情報は必ず環境変数で管理し、Gitにコミットしないでください
2. データベースのバックアップを定期的に取得してください
3. 本番環境へのデプロイ前に必ずテストを実行してください

## トラブルシューティング
1. データベース接続エラー
   - 環境変数の設定を確認
   - データベースサービスの状態を確認

2. アプリケーション起動エラー
   - ログの確認: `journalctl -u golf-recommendation`
   - ポートの使用状況確認: `netstat -tulpn | grep 8000`

3. パフォーマンス問題
   - データベースのインデックス確認
   - クエリの最適化
   - キャッシュの活用 