# メール通知設定
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',  # GmailのSMTPサーバー
    'smtp_port': 587,  # TLS用ポート
    'sender_email': 'your-email@gmail.com',  # 送信元メールアドレス
    'sender_password': 'your-app-password',  # アプリパスワード
    'recipient_emails': [
        'admin1@example.com',
        'admin2@example.com'
    ],
    'subject_prefix': '[GolfClub Backup] '  # メール件名のプレフィックス
} 