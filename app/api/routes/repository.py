from fastapi import APIRouter, Depends
from app.api.dependencies import get_repository_service
from app.schemas.repository import (RepositoryCreateRequest, RepositoryResponse, RepositoryOperationResponse,RepositoryStatusResponse) 

router = APIRouter(prefix="/repositories", tags=["repositories"])

@router.post("/repositories:", response_model=RepositoryOperationResponse)
async def create_repository(
    request: RepositoryCreateRequest,
    RepositoryService = Depends(get_repository_service),
) -> RepositoryOperationResponse:
    """
    Create a new repository by cloning it from the provided GitHub URL.
    """
    repository = RepositoryService.prepare_repository(str(request.github_url))
    return RepositoryOperationResponse(
        message="Repository created successfully.",
        repository=RepositoryResponse(
            Owner=repository.Owner,
            repo_name=repository.repo_name,
            url=repository.url,
            local_path=str(repository.local_path),
        ),
    )

