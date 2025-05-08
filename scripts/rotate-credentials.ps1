param(
    [string]$Environment = "development",
    [string]$Service = "all"
)

# 環境変数ファイルのパス
$envPath = "$env:LOCALAPPDATA\golf-app\env.$Environment"

# バックアップの作成
Copy-Item $envPath "$envPath.backup"

# サービスごとの認証情報ローテーション
switch ($Service) {
    "aws" {
        # AWS認証情報のローテーション
        $newKey = aws iam create-access-key --user-name your-username
        # 環境変数ファイルの更新
        (Get-Content $envPath) -replace "AWS_ACCESS_KEY_ID=.*", "AWS_ACCESS_KEY_ID=$($newKey.AccessKey.AccessKeyId)" | Set-Content $envPath
        (Get-Content $envPath) -replace "AWS_SECRET_ACCESS_KEY=.*", "AWS_SECRET_ACCESS_KEY=$($newKey.AccessKey.SecretAccessKey)" | Set-Content $envPath
    }
    "slack" {
        # Slackトークンのローテーション
        # Slack APIを使用して新しいトークンを生成
        $newToken = "new-slack-token"
        (Get-Content $envPath) -replace "SLACK_BOT_TOKEN=.*", "SLACK_BOT_TOKEN=$newToken" | Set-Content $envPath
    }
    "database" {
        # データベースパスワードのローテーション
        $newPassword = "new-db-password"
        (Get-Content $envPath) -replace "DATABASE_URL=.*", "DATABASE_URL=postgresql://user:$newPassword@localhost:5432/golfclub" | Set-Content $envPath
    }
    "all" {
        # すべての認証情報をローテーション
        # AWS
        $newKey = aws iam create-access-key --user-name your-username
        (Get-Content $envPath) -replace "AWS_ACCESS_KEY_ID=.*", "AWS_ACCESS_KEY_ID=$($newKey.AccessKey.AccessKeyId)" | Set-Content $envPath
        (Get-Content $envPath) -replace "AWS_SECRET_ACCESS_KEY=.*", "AWS_SECRET_ACCESS_KEY=$($newKey.AccessKey.SecretAccessKey)" | Set-Content $envPath
        
        # Slack
        $newToken = "new-slack-token"
        (Get-Content $envPath) -replace "SLACK_BOT_TOKEN=.*", "SLACK_BOT_TOKEN=$newToken" | Set-Content $envPath
        
        # データベース
        $newPassword = "new-db-password"
        (Get-Content $envPath) -replace "DATABASE_URL=.*", "DATABASE_URL=postgresql://user:$newPassword@localhost:5432/golfclub" | Set-Content $envPath
    }
}

# ログの記録
$logPath = "$env:LOCALAPPDATA\golf-app\logs\credential-rotation.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"[$timestamp] Rotated credentials for $Environment environment, $Service service" | Add-Content $logPath 