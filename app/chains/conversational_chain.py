"""Conversational retrieval chain."""

from langchain_core.runnables import Runnable
from langchain_core.runnables.history import RunnableWithMessageHistory

from app.memory.redis_history import RedisHistoryService


class ConversationalChain:
    """
    Wrap a retrieval chain with persistent
    Redis-backed conversation history.
    """

    def __init__(
        self,
        retrieval_chain: Runnable,
        history_service: RedisHistoryService,
    ) -> None:
        self._retrieval_chain = retrieval_chain
        self._history_service = history_service

    def create(self) -> Runnable:
        """
        Create a conversational retrieval chain.
        """

        return RunnableWithMessageHistory(
            runnable=self._retrieval_chain,
            get_session_history=self._history_service.get_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )