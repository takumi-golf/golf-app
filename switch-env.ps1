param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('development', 'production')]
    [string]$Environment
)

# 現在の環境を表示
Write-Host "現在の環境: $($env:ENVIRONMENT)"

# 環境ファイルをコピー
Copy-Item ".env.$Environment" ".env" -Force

# 環境変数を更新
$env:ENVIRONMENT = $Environment

Write-Host "環境を $Environment に切り替えました"
Write-Host "新しい環境: $($env:ENVIRONMENT)" 