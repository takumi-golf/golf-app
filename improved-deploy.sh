#!/bin/bash

# エラーが発生したら即座に終了
set -e

# 色の定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ログ出力関数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 環境変数の設定
FRONTEND_DIR="./frontend"
BACKEND_DIR="./backend"
ENV=${1:-"prod"}  # デフォルトは本番環境
NODE_ENV="production"

# 引数の検証
if [[ ! "$ENV" =~ ^(prod|test)$ ]]; then
    log_error "無効な環境指定です。'prod' または 'test' を指定してください。"
    exit 1
fi

# キャッシュディレクトリの設定
NPM_CACHE_DIR="$FRONTEND_DIR/.npm-cache"
NODE_MODULES_DIR="$FRONTEND_DIR/node_modules"

# フロントエンドのビルド
deploy_frontend() {
    log_info "フロントエンドのデプロイを開始します..."
    cd $FRONTEND_DIR

    # npmキャッシュの設定
    if [ ! -d "$NPM_CACHE_DIR" ]; then
        mkdir -p "$NPM_CACHE_DIR"
    fi

    # package-lock.json の変更チェック
    if [ -f .package-lock-checksum ] && [ "$(md5sum package-lock.json | cut -d ' ' -f 1)" = "$(cat .package-lock-checksum)" ]; then
        log_info "依存関係に変更なし - インストールをスキップします"
    else
        log_info "依存関係が変更されました - パッケージをインストールします"
        # キャッシュを使用して高速インストール
        npm ci --cache "$NPM_CACHE_DIR" --prefer-offline
        md5sum package-lock.json | cut -d ' ' -f 1 > .package-lock-checksum
    fi

    # 環境変数を設定してビルド
    log_info "${ENV}環境用にビルドを開始します..."
    export REACT_APP_ENV=$ENV
    export NODE_ENV=$NODE_ENV
    npm run build

    # ビルド成果物の最適化
    log_info "ビルド成果物を最適化します..."
    cd build
    # 不要なファイルの削除
    find . -name "*.map" -type f -delete
    find . -name "*.ts" -type f -delete
    find . -name "*.tsx" -type f -delete

    log_info "フロントエンドのデプロイが完了しました"
}

# バックエンドのデプロイ
deploy_backend() {
    log_info "バックエンドのデプロイを開始します..."
    cd $BACKEND_DIR

    # 仮想環境の確認と作成
    if [ ! -d ".venv" ]; then
        log_info "仮想環境を作成します..."
        python3 -m venv .venv
    fi

    # 仮想環境のアクティベート
    source .venv/bin/activate

    # 依存関係のインストール
    log_info "依存関係をインストールします..."
    pip install -r requirements.txt

    log_info "バックエンドのデプロイが完了しました"
}

# クリーンアップ関数
cleanup() {
    log_info "クリーンアップを実行します..."
    # 一時ファイルの削除
    find $FRONTEND_DIR -name "*.log" -type f -delete
    find $BACKEND_DIR -name "*.log" -type f -delete
    find $FRONTEND_DIR -name "*.tmp" -type f -delete
    find $BACKEND_DIR -name "*.tmp" -type f -delete
}

# メイン処理
main() {
    log_info "${ENV}環境へのデプロイを開始します..."

    # フロントエンドのデプロイ
    deploy_frontend

    # バックエンドのデプロイ
    deploy_backend

    # クリーンアップ
    cleanup

    log_info "デプロイが完了しました！"
}

# スクリプトの実行
main 