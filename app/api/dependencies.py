"""Shared API dependencies."""
"""Application dependencies."""

from fastapi import Depends
from flashrank import Ranker
from app.core.config import settings

from app.services.repository_service import RepositoryService
from app.services.indexing_service import IndexingService
from app.services.chat_service import ChatService

from app.indexing.repository_loader import RepositoryLoader
from app.indexing.ast_enricher import ASTEnricher
from app.indexing.CodeChunker import CodeChunker

from app.retrieval.Embedding_Service import EmbeddingService
from app.retrieval.Faiss_store import FAISSStore
from app.retrieval.bm25_store import BM25Store
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.reranker import FlashRankReranker

from app.models.llm import ChatModelService
from app.chains.history_aware_retriever import HistoryAwareRetriever
from app.chains.qa_chain import QuestionAnswerChain
from app.chains.retrieval_chain import RetrievalChain
from app.chains.conversational_chain import ConversationalChain
from app.memory.redis_history import RedisHistoryService

ranker = Ranker(model_name=settings.RANKER_MODEL)

def get_repository_service() -> RepositoryService:
    """Get the repository service instance."""
    return RepositoryService()


# ==========================================================
# Indexing Components
# ==========================================================

def get_repository_loader() -> RepositoryLoader:
    return RepositoryLoader()


def get_ast_enricher() -> ASTEnricher:
    return ASTEnricher()


def get_code_chunker() -> CodeChunker:
    return CodeChunker()


def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()


def get_faiss_store(
    embedding_service: EmbeddingService = Depends(get_embedding_service),
) -> FAISSStore:
    return FAISSStore(
        embedding_service=embedding_service,
    )


def get_bm25_store() -> BM25Store:
    return BM25Store()


# ==========================================================
# Retrieval Components
# ==========================================================

def get_hybrid_retriever() -> HybridRetriever:
    return HybridRetriever()


def get_flashrank_reranker() -> FlashRankReranker:
    ranker = Ranker()

    return FlashRankReranker(
        client=ranker,
    )


# ==========================================================
# Chat Model
# ==========================================================

def get_chat_model_service() -> ChatModelService:
    return ChatModelService()


# ==========================================================
# Chains
# ==========================================================

def get_history_aware_retriever(
    chat_model: ChatModelService = Depends(get_chat_model_service),
) -> HistoryAwareRetriever:

    return HistoryAwareRetriever(
        llm=chat_model.model,
    )


def get_question_answer_chain(
    chat_model: ChatModelService = Depends(get_chat_model_service),
) -> QuestionAnswerChain:

    return QuestionAnswerChain(
        llm=chat_model.model,
    )


def get_retrieval_chain() -> RetrievalChain:
    return RetrievalChain()


def get_conversation_chain() -> ConversationalChain:
    return ConversationalChain()


# ==========================================================
# Memory
# ==========================================================

def get_history_service() -> RedisHistoryService:
    return RedisHistoryService()


# ==========================================================
# Indexing Service
# ==========================================================

def get_indexing_service() -> IndexingService:
    return IndexingService()


# ==========================================================
# Chat Service
# ==========================================================

def get_chat_service(
    faiss_store: FAISSStore = Depends(get_faiss_store),
    bm25_store: BM25Store = Depends(get_bm25_store),
    hybrid_retriever: HybridRetriever = Depends(get_hybrid_retriever),
    reranker: FlashRankReranker = Depends(get_flashrank_reranker),
    history_aware_retriever: HistoryAwareRetriever = Depends(get_history_aware_retriever),
    qa_chain: QuestionAnswerChain = Depends(get_question_answer_chain),
    retrieval_chain: RetrievalChain = Depends(get_retrieval_chain),
    conversation_chain: ConversationalChain = Depends(get_conversation_chain),
    history_service: RedisHistoryService = Depends(get_history_service),
) -> ChatService:

    return ChatService(
        faiss_store=faiss_store,
        bm25_store=bm25_store,
        hybrid_retriever=hybrid_retriever,
        reranker=reranker,
        history_aware_retriever=history_aware_retriever,
        qa_chain=qa_chain,
        retrieval_chain=retrieval_chain,
        conversation_chain=conversation_chain,
        history_service=history_service,
    )