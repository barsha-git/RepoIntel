"""FAISS vector store management."""

from pathlib import Path
import shutil

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_community.vectorstores import FAISS

from app.core.config import settings
from app.core.logging import logger
from app.models.repository import Repository
from app.retrieval.Embedding_Service import EmbeddingService


class FAISSStore:
    """Manage FAISS vector stores."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
    ) -> None:
        """Initialize the FAISS store."""
        self.embedding_service = embedding_service

    def create(
        self,
        documents: list[Document],
    ) -> FAISS:
        """
        Create a FAISS vector store from documents.
        """

        logger.info(
            "Creating FAISS index from {} documents.",
            len(documents),
        )

        vector_store = FAISS.from_documents(
            documents,
            self.embedding_service.model,
        )

        logger.success("FAISS index created successfully.")

        return vector_store

    def save(
        self,
        vector_store: FAISS,
        repository: Repository,
    ) -> None:
        """
        Persist a FAISS vector store to disk.
        """

        index_path = self._index_path(repository)

        index_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        logger.info(
            "Saving FAISS index for {}/{}.",
            repository.Owner,
            repository.repo_name,
        )

        vector_store.save_local(
            folder_path=str(index_path),
        )

        logger.success("FAISS index saved successfully.")

    def load(
        self,
        repository: Repository,
    ) -> FAISS:
        """
        Load a persisted FAISS vector store.
        """

        index_path = self._index_path(repository)

        logger.info(
            "Loading FAISS index for {}/{}.",
            repository.Owner,
            repository.repo_name,
        )

        vector_store = FAISS.load_local(
            folder_path=str(index_path),
            embeddings=self.embedding_service.model,
            allow_dangerous_deserialization=True,
        )

        logger.success("FAISS index loaded successfully.")

        return vector_store

    def exists(
        self,
        repository: Repository,
    ) -> bool:
        """
        Check whether a FAISS index exists.
        """

        index_path = self._index_path(repository)

        return (
            (index_path / "index.faiss").exists()
            and (index_path / "index.pkl").exists()
        )

    def delete(
        self,
        repository: Repository,
    ) -> None:
        """
        Delete a persisted FAISS index.
        """

        index_path = self._index_path(repository)

        if not index_path.exists():
            return

        logger.info(
            "Deleting FAISS index for {}/{}.",
            repository.Owner,
            repository.repo_name,
        )

        shutil.rmtree(index_path)

        logger.success("FAISS index deleted successfully.")

    def as_retriever(
        self,
        vector_store: FAISS,
        k: int = 5,
    ) -> VectorStoreRetriever:
        """
        Convert a FAISS vector store into a retriever.
        """

        return vector_store.as_retriever(
            search_kwargs={
                "k": k,
            },
        )

    def _index_path(
        self,
        repository: Repository,
    ) -> Path:
        """
        Return the storage path for a repository's FAISS index.
        """

        return (
            Path(settings.STORAGE_PATH)
            / "indexes"
            / "faiss"
            / repository.Owner
            / repository.repo_name
        )