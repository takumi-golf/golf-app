# Slack通知設定
SLACK_CONFIG = {
    'webhook_url': 'https://hooks.slack.com/services/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',
    'channel': '#backup-notifications',  # 通知を送信するチャンネル
    'username': 'GolfClub Backup Bot',  # ボットの表示名
    'icon_emoji': ':floppy_disk:',  # ボットのアイコン
    'notification_settings': {
        'start_backup': True,  # バックアップ開始通知
        'db_type': True,  # データベース種別通知
        'progress': True,  # 進捗通知
        'success': True,  # 成功通知
        'error': True,  # エラー通知
        'cleanup': True  # 古いバックアップ削除通知
    }
} 