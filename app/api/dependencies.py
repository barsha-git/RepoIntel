from app.services.repository_service import RepositoryService
from app.services.indexing_service import IndexingService


def get_repository_service() -> RepositoryService:
    """
    Return the repository service.

    This function is used as a dependency in FastAPI routes.
    """

    return RepositoryService()

def get_indexing_service() -> IndexingService:
    """get the indexing service instance"""
    return IndexingService()

