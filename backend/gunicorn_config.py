import multiprocessing

# ワーカープロセスの数
workers = multiprocessing.cpu_count() * 2 + 1

# ワーカークラス
worker_class = "uvicorn.workers.UvicornWorker"

# バインドアドレス
bind = "0.0.0.0:8000"

# タイムアウト設定
timeout = 120

# アクセスログ
accesslog = "logs/access.log"
errorlog = "logs/error.log"

# デーモンモード
daemon = False

# リロード設定
reload = True 