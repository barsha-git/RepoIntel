from app.services.repository_service import RepositoryService

def get_repository_service() -> RepositoryService:
    """
    Return the repository service.

    This function is used as a dependency in FastAPI routes.
    """

    return RepositoryService()

