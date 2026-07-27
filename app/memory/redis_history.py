"""Redis-backed chat message history service."""

from langchain_redis import RedisChatMessageHistory

from app.core.config import settings


class RedisHistoryService:
    """
    Manage chat histories stored in Redis.

    This service acts as a thin wrapper around
    RedisChatMessageHistory so the rest of the
    application never interacts with Redis directly.
    """

    def __init__(self) -> None:
        """Initialize the history service."""

        self.redis_url = settings.REDIS_URL
        self.ttl = settings.HISTORY_TTL
        self.key_prefix = settings.HISTORY_KEY_PREFIX

    def get_history(
        self,
        session_id: str,
    ) -> RedisChatMessageHistory:
        """
        Return the chat history for a session.

        If the session does not exist,
        RedisChatMessageHistory creates it automatically.
        """

        return RedisChatMessageHistory(
            session_id=f"{self.key_prefix}{session_id}",
            redis_url=self.redis_url,
            ttl=self.ttl,
        )

    def clear_history(
        self,
        session_id: str,
    ) -> None:
        """
        Remove all messages from a session.
        """

        history = self.get_history(session_id)

        history.clear()

    def delete_history(
        self,
        session_id: str,
    ) -> None:
        """
        Delete a session history.

        Alias of clear_history() because RedisChatMessageHistory
        removes all stored messages when cleared.
        """

        self.clear_history(session_id)

    def history_exists(
        self,
        session_id: str,
    ) -> bool:
        """
        Check whether a session contains messages.
        """

        history = self.get_history(session_id)

        return len(history.messages) > 0