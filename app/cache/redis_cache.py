class RedisCache:
    def __init__(self, client=None):
        self.client = client

    def get(self, key: str):
        if self.client is not None:
            return self.client.get(key)
        return None

    def set(self, key: str, value: object) -> None:
        if self.client is not None:
            self.client.set(key, value)
