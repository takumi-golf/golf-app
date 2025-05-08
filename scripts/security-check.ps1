# 環境変数ファイルの権限チェック
function Test-EnvironmentFiles {
    $envFiles = Get-ChildItem "$env:LOCALAPPDATA\golf-app\env.*"
    foreach ($file in $envFiles) {
        $acl = Get-Acl $file.FullName
        if ($acl.Access.FileSystemRights -match "FullControl") {
            Write-Warning "File $($file.Name) has too permissive permissions"
        }
    }
}

# 認証情報の有効期限チェック
function Test-CredentialExpiration {
    $logPath = "$env:LOCALAPPDATA\golf-app\logs\credential-rotation.log"
    if (Test-Path $logPath) {
        $lastRotation = Get-Content $logPath -Tail 1
        $rotationDate = [datetime]::ParseExact($lastRotation.Split('[')[1].Split(']')[0], "yyyy-MM-dd HH:mm:ss", $null)
        if ((Get-Date).Subtract($rotationDate).TotalDays -gt 30) {
            Write-Warning "Credentials have not been rotated in over 30 days"
        }
    }
}

# アクセスログの確認
function Test-AccessLogs {
    $logPath = "$env:LOCALAPPDATA\golf-app\logs\access.log"
    if (Test-Path $logPath) {
        $recentLogs = Get-Content $logPath -Tail 100
        $suspiciousActivities = $recentLogs | Where-Object { $_ -match "failed login|unauthorized access" }
        if ($suspiciousActivities) {
            Write-Warning "Suspicious activities detected in access logs"
        }
    }
}

# セキュリティアップデートの確認
function Test-SecurityUpdates {
    $updates = Get-HotFix | Where-Object { $_.InstalledOn -gt (Get-Date).AddDays(-7) }
    if (-not $updates) {
        Write-Warning "No security updates installed in the last 7 days"
    }
}

# メインのチェック実行
Write-Host "Starting security check..."
Test-EnvironmentFiles
Test-CredentialExpiration
Test-AccessLogs
Test-SecurityUpdates
Write-Host "Security check completed." 