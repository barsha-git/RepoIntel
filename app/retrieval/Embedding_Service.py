from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingService:
    """Manage the application's embedding model."""

    def __init__(self) -> None:
        """Initialize the embedding model."""
        self._model = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            model_kwargs={
                "device": "cpu",
            },
            encode_kwargs={
                "normalize_embeddings": True,
            },
        )

    @property
    def model(self) -> HuggingFaceEmbeddings:
        """
        Return the configured embedding model.

        This is used by vector stores such as FAISS.
        """
        return self._model

    def embed_query(self, query: str) -> list[float]:
        """
        Generate an embedding vector for a user query.
        """
        return self._model.embed_query(query)

    def embed_documents(self,documents: list[Document]) -> list[list[float]]:
        """
        Generate embedding vectors for a list of documents.
        """

        texts = [
            document.page_content
            for document in documents
        ]

        return self._model.embed_documents(texts)