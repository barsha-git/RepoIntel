"""Chat service."""

from typing import Any

from app.models.repository import Repository

from app.retrieval.Faiss_store import FAISSStore
from app.retrieval.bm25_store import BM25Store
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.reranker import FlashRankReranker

from app.chains.history_aware_retriever import HistoryAwareRetriever
from app.chains.qa_chain import QuestionAnswerChain
from app.chains.retrieval_chain import RetrievalChain
from app.chains.conversational_chain import ConversationalChain
from app.memory.redis_history import RedisHistoryService
from langchain_core.runnables import Runnable

class ChatService:
    """
    Orchestrates the complete conversational RAG pipeline.

    The retrieval pipeline is cached per repository so it is built only once.
    """

    def __init__(
        self,
        faiss_store: FAISSStore,
        bm25_store: BM25Store,
        hybrid_retriever: HybridRetriever,
        reranker: FlashRankReranker,
        history_aware_retriever: HistoryAwareRetriever,
        qa_chain: QuestionAnswerChain,
        retrieval_chain: RetrievalChain,
        conversation_chain: ConversationalChain,
        history_service: RedisHistoryService,
    ) -> None:

        self.faiss_store = faiss_store
        self.bm25_store = bm25_store

        self.hybrid_retriever = hybrid_retriever
        self.reranker = reranker

        self.history_aware_retriever = history_aware_retriever
        self.qa_chain = qa_chain
        self.retrieval_chain = retrieval_chain
        self.conversation_chain = conversation_chain
        self.history_service = history_service

        self._pipeline_cache: dict[str, Any] = {}

    def _cache_key(
        self,
        repository: Repository,
    ) -> str:
        """Return a unique cache key."""

        return f"{repository.Owner}/{repository.repo_name}"

    def _build_pipeline(
        self,
        repository: Repository,
    ) -> Runnable:
        """
        Build the complete retrieval pipeline.
        """

        # ----------------------------
        # Load FAISS
        # ----------------------------
        vector_store = self.faiss_store.load(repository)

        faiss_retriever = self.faiss_store.as_retriever(
            vector_store,
        )

        # ----------------------------
        # Load BM25
        # ----------------------------
        bm25_retriever = self.bm25_store.load(repository)

        # ----------------------------
        # Hybrid Retrieval
        # ----------------------------
        hybrid = self.hybrid_retriever.create(
            faiss_retriever=faiss_retriever,
            bm25_retriever=bm25_retriever,
        )

        # ----------------------------
        # FlashRank
        # ----------------------------
        reranker = self.reranker.create(
            retriever=hybrid,
        )

        # ----------------------------
        # History-aware Retriever
        # ----------------------------
        history = self.history_aware_retriever.create(
            retriever=reranker,
        )

        # ----------------------------
        # Retrieval Chain
        # ----------------------------
        retrieval = self.retrieval_chain.create(
            retriever=history,
            qa_chain=self.qa_chain.create(),
        )

        return retrieval

    def _get_pipeline(
        self,
        repository: Repository,
    ) -> Runnable:
        """
        Return a cached pipeline if available.
        """

        key = self._cache_key(repository)

        if key not in self._pipeline_cache:
            self._pipeline_cache[key] = self._build_pipeline(
                repository,
            )

        return self._pipeline_cache[key]

    def chat(
        self,
        repository: Repository,
        question: str,
        session_id: str,
    ):
        """
        Execute a conversational RAG query.
        """

        retrieval = self._get_pipeline(repository)

        conversation = self.conversation_chain.create(
            retrieval_chain=retrieval,
            history_service=self.history_service,
        )

        return conversation.invoke(
            {
                "input": question,
            },
            config={
                "configurable": {
                    "session_id": session_id,
                }
            },
        )

    def invalidate_cache(
        self,
        repository: Repository,
    ) -> None:
        """
        Remove a repository pipeline from cache.
        """

        self._pipeline_cache.pop(
            self._cache_key(repository),
            None,
        )