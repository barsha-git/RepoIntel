"""Retrieval chain."""

from langchain.chains import create_retrieval_chain
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import Runnable


class RetrievalChain:
    """
    Compose the history-aware retriever and
    question-answer chain into a single runnable.
    """

    def __init__(
        self,
        retriever: BaseRetriever,
        qa_chain: Runnable,
    ) -> None:
        self._retriever = retriever
        self._qa_chain = qa_chain

    def create(self) -> Runnable:
        """
        Create the retrieval chain.
        """

        return create_retrieval_chain(
            retriever=self._retriever,
            combine_docs_chain=self._qa_chain,
        )