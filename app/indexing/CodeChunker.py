"""Text Chunker for Code Documents"""

from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_core.documents import Document

class CodeChunker:
    def chunk(self, documents: list[Document]) -> list[Document]:
        chunk =[]
        for document in documents:
            extension = document.metadata.get("extension")
            if extension == ".py":
                chunk.extend(self._chunk_python_document(document))
            elif extension == ".md":
                chunk.extend(self._chunk_markdown_document(document))
            else:
                chunk.extend(self.chunk_generic_document(document))
        return chunk

    def _chunk_python_document(self, document: Document) -> list[Document]:
        """Chunk a python doc into smaller pieces"""
        textsplitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON,
            chunk_size=1000,
            chunk_overlap=200,
        )
        return textsplitter.split_documents([document])

    def _chunk_markdown_document(self, document: Document) -> list[Document]:
        """Chunk a markdown doc into smaller pieces"""
        textsplitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.MARKDOWN,
            chunk_size=1000,
            chunk_overlap=200,
        )
        return textsplitter.split_documents([document])

    def chunk_generic_document(self, document: Document) -> list[Document]:
        """Chunk a generic doc into smaller pieces"""
        textsplitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        return textsplitter.split_documents([document])

