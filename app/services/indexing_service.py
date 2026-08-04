from app.indexing.repository_loader import RepositoryLoader
from app.indexing.ast_enricher import ASTEnricher
from app.indexing.CodeChunker import CodeChunker
from app.retrieval.Embedding_Service import EmbeddingService
from app.retrieval.bm25_store import BM25Store
from app.retrieval.Faiss_store import FAISSStore

from app.core.logging import logger

class IndexingService:

    def __init__(self):
       """Initialize the indexing service."""
       self.loader = RepositoryLoader()
       self.enricher = ASTEnricher()
       self.chunker = CodeChunker()
       self.embedding_service = EmbeddingService()
       self.faiss_store = FAISSStore(self.embedding_service)
       self.bm25_store = BM25Store()

    def index_repository(self, repository): 
       """
    Index a Git repository by loading, enriching, chunking, and storing its code.

    Args:
        repository (Repository): The repository to index."""
       
       logger.info(f"Indexing repository: {repository.repo_name} owned by {repository.Owner}")
       documents = self.loader.load(repository)
       logger.success(f"Loaded {len(documents)} documents from repository: {repository.repo_name}")

       logger.info(f"Enriching documents with AST metadata: {repository.repo_name}")
       enriched_documents = self.enricher.enrich(documents)
       logger.success(f"Enriched {len(enriched_documents)} documents with AST metadata: {repository.repo_name}")

       logger.info(f"Chunking documents: {repository.repo_name}")
       chunks = self.chunker.chunk(enriched_documents)
       logger.success(f"Created {len(chunks)} chunks from enriched documents: {repository.repo_name}")

       logger.info(f"Creating FAISS vector store from chunks: {repository.repo_name}")
       vector_store = self.faiss_store.create(chunks)
       logger.success(f"FAISS vector store created successfully: {repository.repo_name}")

       logger.info(f"Saving FAISS vector store to disk: {repository.repo_name}")
       self.faiss_store.save(vector_store, repository)
       logger.success(f"FAISS vector store saved to disk successfully: {repository.repo_name}")

       logger.info(f"Creating BM25 store from chunks: {repository.repo_name}")
       bm25_store= self.bm25_store.create(chunks)
       logger.success(f"BM25 store created successfully: {repository.repo_name}")

       logger.info(f"Saving BM25 store to disk: {repository.repo_name}")
       self.bm25_store.save(bm25_store, repository)
       logger.success(f"BM25 store saved to disk successfully: {repository.repo_name}")

       return {
         "message": "Repository indexed successfully.",
         "repository": repository.repo_name,
         "indexed_documents": len(chunks),
         "chunks": len(chunks),
         "status": "success"
        }
    
    


