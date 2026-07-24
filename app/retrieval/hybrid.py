"""Hybrid retriever."""

from langchain_core.retrievers import BaseRetriever, EnsembleRetriever


class HybridRetriever:
    """Combine semantic and keyword retrievers."""

    def __init__(
        self,
        faiss_weight: float = 0.6,
        bm25_weight: float = 0.4,
    ) -> None:
        """
        Initialize hybrid retriever.

        Args:
            faiss_weight: Weight assigned to FAISS retrieval.
            bm25_weight: Weight assigned to BM25 retrieval.
        """
        self.faiss_weight = faiss_weight
        self.bm25_weight = bm25_weight

    def create(
        self,
        faiss_retriever: BaseRetriever,
        bm25_retriever: BaseRetriever,
    ) -> EnsembleRetriever:
        """
        Create a hybrid retriever.
        """

        return EnsembleRetriever(
            retrievers=[
                faiss_retriever,
                bm25_retriever,
            ],
            weights=[
                self.faiss_weight,
                self.bm25_weight,
            ],
        )

    def update_weights(
        self,
        *,
        faiss_weight: float,
        bm25_weight: float,
    ) -> None:
        """
        Update retrieval weights.
        """

        self.faiss_weight = faiss_weight
        self.bm25_weight = bm25_weight
