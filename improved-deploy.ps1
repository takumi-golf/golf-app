# エラーが発生したら即座に終了
$ErrorActionPreference = "Stop"

# 色の定義
$RED = [System.ConsoleColor]::Red
$GREEN = [System.ConsoleColor]::Green
$YELLOW = [System.ConsoleColor]::Yellow

# ログ出力関数
function Write-LogInfo {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor $GREEN
}

function Write-LogWarn {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor $YELLOW
}

function Write-LogError {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $RED
}

# 環境変数の設定
$FRONTEND_DIR = ".\frontend"
$BACKEND_DIR = ".\backend"
$ENV = if ($args[0]) { $args[0] } else { "prod" }  # デフォルトは本番環境
$NODE_ENV = "production"

# 引数の検証
if ($ENV -notmatch "^(prod|test)$") {
    Write-LogError "Invalid environment specified. Please use 'prod' or 'test'."
    exit 1
}

# キャッシュディレクトリの設定
$NPM_CACHE_DIR = Join-Path $FRONTEND_DIR ".npm-cache"
$NODE_MODULES_DIR = Join-Path $FRONTEND_DIR "node_modules"

# フロントエンドのビルド
function Deploy-Frontend {
    Write-LogInfo "Starting frontend deployment..."
    Push-Location $FRONTEND_DIR

    try {
        # npmキャッシュの設定
        if (-not (Test-Path $NPM_CACHE_DIR)) {
            New-Item -ItemType Directory -Path $NPM_CACHE_DIR -Force | Out-Null
        }

        # node_modulesのクリーンアップ
        if (Test-Path $NODE_MODULES_DIR) {
            Write-LogInfo "Cleaning up node_modules..."
            Remove-Item -Path $NODE_MODULES_DIR -Recurse -Force -ErrorAction SilentlyContinue
        }

        # package-lock.json の変更チェック
        $packageLockPath = "package-lock.json"
        $checksumPath = ".package-lock-checksum"
        
        if ((Test-Path $checksumPath) -and 
            (Get-FileHash $packageLockPath -Algorithm MD5).Hash -eq (Get-Content $checksumPath)) {
            Write-LogInfo "No changes in dependencies - skipping installation"
        } else {
            Write-LogInfo "Dependencies have changed - installing packages"
            # キャッシュを使用して高速インストール
            npm ci --cache $NPM_CACHE_DIR --prefer-offline
            (Get-FileHash $packageLockPath -Algorithm MD5).Hash | Set-Content $checksumPath
        }

        # 環境変数を設定してビルド
        Write-LogInfo "Starting build for $ENV environment..."
        $env:REACT_APP_ENV = $ENV
        $env:NODE_ENV = $NODE_ENV
        $env:GENERATE_SOURCEMAP = "false"
        npm run build

        # ビルド成果物の最適化
        Write-LogInfo "Optimizing build artifacts..."
        Set-Location build
        # 不要なファイルの削除
        Get-ChildItem -Recurse -Include "*.map","*.ts","*.tsx" | Remove-Item -Force

        Write-LogInfo "Frontend deployment completed"
    }
    finally {
        Pop-Location
    }
}

# バックエンドのデプロイ
function Deploy-Backend {
    Write-LogInfo "Starting backend deployment..."
    Push-Location $BACKEND_DIR

    try {
        # 仮想環境の確認と作成
        if (-not (Test-Path ".venv")) {
            Write-LogInfo "Creating virtual environment..."
            python -m venv .venv
        }

        # 仮想環境のアクティベート
        & .\.venv\Scripts\Activate.ps1

        # 依存関係のインストール
        Write-LogInfo "Installing dependencies..."
        pip install -r requirements.txt

        Write-LogInfo "Backend deployment completed"
    }
    finally {
        Pop-Location
    }
}

# クリーンアップ関数
function Cleanup {
    Write-LogInfo "Running cleanup..."
    # 一時ファイルの削除
    Get-ChildItem -Path $FRONTEND_DIR -Recurse -Include "*.log","*.tmp" | Remove-Item -Force
    Get-ChildItem -Path $BACKEND_DIR -Recurse -Include "*.log","*.tmp" | Remove-Item -Force
}

# メイン処理
function Main {
    Write-LogInfo "Starting deployment for $ENV environment..."

    # フロントエンドのデプロイ
    Deploy-Frontend

    # バックエンドのデプロイ
    Deploy-Backend

    # クリーンアップ
    Cleanup

    Write-LogInfo "Deployment completed!"
}

# スクリプトの実行
Main 