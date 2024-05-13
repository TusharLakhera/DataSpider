from abc import ABC, abstractmethod
from typing import Dict, Any

class Cache(ABC):
    @abstractmethod
    def get(self, key: str) -> Any:
        pass

    @abstractmethod
    def set(self, key: str, value: Any):
        pass

class RedisCache(Cache):
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def get(self, key: str) -> Any:
        return self.redis_client.get(key)

    def set(self, key: str, value: Any):
        self.redis_client.set(key, value)