from fastapi import APIRouter, Depends, HTTPException
from pathlib import Path
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

@router.get("/{owner}/{name}", response_model=RepositoryResponse)
def get_repository(
    owner: str,
    name: str,
    repository_service = Depends(get_repository_service),
):
    repo = repository_service.get_repository(owner, name)

    return RepositoryResponse(
        Owner=repo.Owner,
        repo_name=repo.repo_name,
        url=repo.url,
        local_path=str(repo.local_path),
    )

@router.patch("/{owner}/{name}", response_model=RepositoryOperationResponse)
def update_repository(
    owner: str,
    name: str,
    repository_service = Depends(get_repository_service),
):
    """
    Update an existing repository by pulling the latest changes from the remote.
    """
    repo = repository_service.get_repository(owner, name)
    repository_service.update_repository(repo)

    return RepositoryOperationResponse(
        message="Repository updated successfully.",
        repository=RepositoryResponse(
            Owner=repo.Owner,
            repo_name=repo.repo_name,
            url=repo.url,
            local_path=str(repo.local_path),
        ),
    )

@router.delete("/{owner}/{name}", response_model=RepositoryOperationResponse)
def delete_repository(
    owner: str,
    name: str,
    repository_service = Depends(get_repository_service),
):
    """
    Delete an existing repository from the local storage.
    """
    repo = repository_service.get_repository(owner, name)
    repository_service.delete_repository(repo)

    return RepositoryOperationResponse(
        message="Repository deleted successfully.",
        repository=RepositoryResponse(
            Owner=repo.Owner,
            repo_name=repo.repo_name,
            url=repo.url,
            local_path=str(repo.local_path),
        ),
    )


