from fastapi import APIRouter, Depends
from app.api.dependencies import get_repository_service, get_indexing_service, get_chat_service
from app.schemas.chat import chatRequest, chatResponse

router = APIRouter(prefix="/chat", tags=["Chat"])
@router.post("/{owner}/{repo_name}", response_model=chatResponse)
def chat_with_repository(
    owner: str,
    repo_name: str,
    request: chatRequest,
    repository_service = Depends(get_repository_service),
    chat_service = Depends(get_chat_service),
):
    """
    chat_with_repository handles a chat request for a specific repository. It retrieves the repository and executes a conversational RAG query using the provided question and session ID.
    """
    repo = repository_service.get_repository(owner, repo_name)
    repository = repository_service.get_repository(owner, repo_name)
    return chat_service.chat(repository, request.message, request.session_id)