class RedisHistory:
    def __init__(self, client=None):
        self.client = client

    def save(self, value: str) -> None:
        if self.client is not None:
            self.client.set(value, value)
