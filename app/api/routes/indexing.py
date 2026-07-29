from fastapi import APIRouter, Depends, HTTPException
from pathlib import Path
from app.api.dependencies import get_repository_service, get_indexing_service
from app.schemas.indexing import IndexingRequest


router = APIRouter(prefix="/indexing", tags=["indexing"])

@router.post("/{owner}/{name}/index", response_model=IndexingRequest)
async def index_repository(
    owner: str,
    name: str,
    repository_service = Depends(get_repository_service),
    indexing_service= Depends(get_indexing_service),
):
    """
    Index a repository by loadig, enriching, chunking, and storing its code"""
    repo = repository_service.get_repository(owner,name)
    result = indexing_service.index_repository(repo)

    return result