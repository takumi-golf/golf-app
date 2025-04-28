from functools import wraps
from datetime import datetime, timedelta
import hashlib
import json
import logging
from typing import Any, Callable, Dict, Optional, Tuple, Union

# キャッシュ設定
CACHE_TTL = 3600  # 1時間
MAX_CACHE_SIZE = 1000  # 最大キャッシュエントリ数
CACHE_CLEANUP_INTERVAL = 300  # 5分ごとにクリーンアップ

class CacheManager:
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._last_cleanup = datetime.now()
        self._setup_logging()

    def _setup_logging(self):
        self.logger = logging.getLogger('cache_manager')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler('cache.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _generate_cache_key(self, func: Callable, *args, **kwargs) -> str:
        """キャッシュキーを生成"""
        key_parts = [
            func.__module__,
            func.__name__,
            str(args),
            str(sorted(kwargs.items()))
        ]
        return hashlib.md5(''.join(key_parts).encode()).hexdigest()

    def _cleanup_cache(self):
        """古いキャッシュエントリを削除"""
        now = datetime.now()
        if (now - self._last_cleanup).seconds < CACHE_CLEANUP_INTERVAL:
            return

        self._last_cleanup = now
        expired_keys = []
        for key, value in self._cache.items():
            if value['expires_at'] < now:
                expired_keys.append(key)

        for key in expired_keys:
            del self._cache[key]
            self.logger.info(f"キャッシュエントリを削除: {key}")

        # キャッシュサイズが大きすぎる場合は古いエントリを削除
        if len(self._cache) > MAX_CACHE_SIZE:
            sorted_items = sorted(
                self._cache.items(),
                key=lambda x: x[1]['created_at']
            )
            for key, _ in sorted_items[:len(self._cache) - MAX_CACHE_SIZE]:
                del self._cache[key]
                self.logger.info(f"キャッシュサイズ制限により削除: {key}")

    def get(self, key: str) -> Optional[Any]:
        """キャッシュから値を取得"""
        self._cleanup_cache()
        if key in self._cache:
            entry = self._cache[key]
            if entry['expires_at'] > datetime.now():
                self.logger.debug(f"キャッシュヒット: {key}")
                return entry['value']
            else:
                del self._cache[key]
                self.logger.debug(f"キャッシュ期限切れ: {key}")
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """キャッシュに値を設定"""
        self._cleanup_cache()
        ttl = ttl or CACHE_TTL
        self._cache[key] = {
            'value': value,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(seconds=ttl)
        }
        self.logger.debug(f"キャッシュ設定: {key}")

    def delete(self, key: str) -> None:
        """キャッシュから値を削除"""
        if key in self._cache:
            del self._cache[key]
            self.logger.info(f"キャッシュ削除: {key}")

    def clear(self) -> None:
        """キャッシュをクリア"""
        self._cache.clear()
        self.logger.info("キャッシュをクリアしました")

# グローバルキャッシュマネージャーインスタンス
cache = CacheManager()

def cached(ttl: Optional[int] = None, key_prefix: Optional[str] = None):
    """キャッシュデコレータ"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # キャッシュキーの生成
            cache_key = cache._generate_cache_key(func, *args, **kwargs)
            if key_prefix:
                cache_key = f"{key_prefix}:{cache_key}"

            # キャッシュから値を取得
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # キャッシュにない場合は関数を実行
            result = func(*args, **kwargs)
            
            # 結果をキャッシュに保存
            cache.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator

def invalidate_cache(key_prefix: str) -> None:
    """指定されたプレフィックスを持つキャッシュを無効化"""
    keys_to_delete = [key for key in cache._cache.keys() if key.startswith(key_prefix)]
    for key in keys_to_delete:
        cache.delete(key)
    cache.logger.info(f"キャッシュを無効化: {key_prefix} ({len(keys_to_delete)} エントリ)") 