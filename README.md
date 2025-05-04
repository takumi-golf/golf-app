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