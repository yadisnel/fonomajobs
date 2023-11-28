import logging
import os

import redis

logger = logging.getLogger(__name__)


class RedisManager:
    # Singleton instance
    _self = None
    redis = None

    # Singleton instance
    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        host = os.getenv("REDIS_HOST")
        if host:
            self.redis = redis.Redis(host=host, port=6379, db=0)
        if not self.enabled():
            logger.warning("Redis is not enabled.")
        else:
            logger.info("Redis is enabled.")

    def get(self, key):
        if self.redis:
            return self.redis.get(key)
        return None

    def set(self, key, value):
        if self.redis:
            return self.redis.set(key, value)
        return None

    def delete(self, key):
        if self.redis:
            return self.redis.delete(key)
        return None

    def enabled(self):
        return self.redis is not None
