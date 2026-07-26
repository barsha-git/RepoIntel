"""History-aware retriever."""

from langchain.chains import create_history_aware_retriever
from langchain_core.language_models import BaseChatModel
from langchain_core.retrievers import BaseRetriever

from app.prompts import contextualize_prompt


class HistoryAwareRetriever:
    """
    Build a history-aware retriever.

    Rewrites follow-up questions into standalone questions
    before retrieving documents.
    """

    def __init__(
        self,
        llm: BaseChatModel,
    ) -> None:
        self._llm = llm

    def create(
        self,
        retriever: BaseRetriever,
    ) -> BaseRetriever:
        """
        Create a history-aware retriever.
        """

        return create_history_aware_retriever(
            llm=self._llm,
            retriever=retriever,
            prompt=contextualize_prompt.CONTEXTUALIZE_PROMPT,
        )