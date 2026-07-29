from pydantic import BaseModel, Field

class IndexingRequest(BaseModel):
    message:str
    repository: str
    indexed_documents: int
    chunks: int
    status: str
    