from collections import deque


class ChatHistory:
    def __init__(self, max_items: int = 10):
        self._history = deque(maxlen=max_items)

    def add(self, message: str) -> None:
        self._history.append(message)

    def get(self) -> list[str]:
        return list(self._history)
