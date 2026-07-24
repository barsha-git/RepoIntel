"""BM25 retriever management."""

from pathlib import Path
import pickle
import shutil

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_community.retrievers import BM25Retriever

from app.core.config import settings
from app.core.logging import logger
from app.models.repository import Repository


class BM25Store:
    """Manage BM25 retrievers."""

    def create(self, documents: list[Document], k: int = 5) -> BM25Retriever:
        """
        Create a BM25 retriever from documents.
        """

        logger.info(
            "Creating BM25 retriever from {} documents.",
            len(documents),
        )

        retriever = BM25Retriever.from_documents(documents)
        retriever.k = k

        logger.success("BM25 retriever created successfully.")

        return retriever

    def save(
        self,
        retriever: BM25Retriever,
        repository: Repository,
    ) -> None:
        """
        Persist the BM25 retriever to disk.
        """

        index_path = self._index_path(repository)
        index_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = index_path / "bm25.pkl"

        logger.info(
            "Saving BM25 retriever for {}/{}.",
            repository.Owner,
            repository.repo_name,
        )

        with open(file_path, "wb") as file:
            pickle.dump(retriever, file)

        logger.success("BM25 retriever saved successfully.")

    def load(
        self,
        repository: Repository,
    ) -> BM25Retriever:
        """
        Load a persisted BM25 retriever.
        """

        file_path = self._index_path(repository) / "bm25.pkl"

        logger.info(
            "Loading BM25 retriever for {}/{}.",
            repository.Owner,
            repository.repo_name,
        )

        with open(file_path, "rb") as file:
            retriever: BM25Retriever = pickle.load(file)

        logger.success("BM25 retriever loaded successfully.")

        return retriever

    def exists(
        self,
        repository: Repository,
    ) -> bool:
        """
        Check whether a BM25 retriever exists.
        """

        file_path = self._index_path(repository) / "bm25.pkl"

        return file_path.exists()

    def delete(self, repository: Repository) -> None:
        """
        Delete the persisted BM25 retriever.
        """

        index_path = self._index_path(repository)

        if not index_path.exists():
            return

        logger.info(
            "Deleting BM25 retriever for {}/{}.",
            repository.Owner,
            repository.repo_name,
        )

        shutil.rmtree(index_path)

        logger.success("BM25 retriever deleted successfully.")

    def as_retriever(self, retriever: BM25Retriever) -> BaseRetriever:
        """
        Return the BM25 retriever.

        This method exists to keep the public API
        consistent with FAISSStore.
        """

        return retriever

    def _index_path(self, repository: Repository) -> Path:
        """
        Return the storage path for the BM25 index.
        """

        return (
            Path(settings.STORAGE_PATH)
            / "indexes"
            / "bm25"
            / repository.Owner
            / repository.repo_name
        )