from pydantic import BaseModel, HttpUrl

class RepositoryCreateRequest(BaseModel):
    github_url: HttpUrl

class RepositoryResponse(BaseModel):
    Owner:str
    repo_name:str
    url:str
    local_path:str

class RepositoryOperationResponse(BaseModel):
    message: str
    repository: RepositoryResponse

class RepositoryStatusResponse(BaseModel):
    Owner:str
    repo_name:str
    exists: bool
    local_path:str
