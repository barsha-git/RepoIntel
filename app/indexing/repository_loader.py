from pathlib import Path
from app.models.repository import Repository
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader, UnstructuredFileLoader
from langchain_core.documents import Document

DEFAULT_EXCLUDE = [
    ".git/**",
    ".github/**",
    "__pycache__/**",
    ".venv/**",
    "venv/**",
    "node_modules/**",
    "dist/**",
    "build/**",
]

class RepositoryLoader:
    """Load repository files into LangChain Documents."""

    def load(self, repository: Repository) -> list[Document]:

        loader = DirectoryLoader(
            path=str(repository.local_path),
            glob="**/*",
            loader_cls=TextLoader,
            recursive=True,
            silent_errors=False,
            exclude=DEFAULT_EXCLUDE,
        )

        documents = loader.load()

        enriched_documents = []

        for document in documents:
            enriched_documents.append(
                self._attach_basic_metadata(
                    document,
                    repository,
                )
            )

        return enriched_documents

    def _attach_basic_metadata(
        self,
        document: Document,
        repository: Repository,
    ) -> Document:
        """
        Attach repository metadata to every document.
        """

        source = Path(document.metadata["source"])

        document.metadata.update(
            {
                "repository": repository.repo_name,
                "owner": repository.Owner,
                "extension": source.suffix,
                "filename": source.name,
                "relative_path": str(
                    source.relative_to(repository.local_path)
                ),
                "is_code": source.suffix
                in {
                    ".py",
                    ".js",
                    ".ts",
                    ".java",
                    ".go",
                    ".rs",
                    ".cpp",
                    ".c",
                    ".cs",
                },
            }
        )

        return document