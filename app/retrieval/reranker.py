"""FlashRank reranker."""

from langchain_core.retrievers import ContextualCompressionRetriever
from langchain_community.document_compressors import FlashrankRerank
from langchain_core.retrievers import BaseRetriever


class FlashRankReranker:
    """Create a FlashRank-powered compression retriever."""

    def __init__(
        self,
        client,
        top_n: int = 3,
    ) -> None:
        """
        Initialize the reranker.

        Args:
            client: FlashRank client instance.
            top_n: Number of documents to keep after reranking.
        """
        self.top_n = top_n
        self._compressor = FlashrankRerank(client=client, top_n=top_n)

    def create(
        self,
        retriever: BaseRetriever,
    ) -> ContextualCompressionRetriever:
        """
        Wrap a retriever with FlashRank reranking.
        """

        return ContextualCompressionRetriever(
            base_compressor=self._compressor,
            base_retriever=retriever,
        )