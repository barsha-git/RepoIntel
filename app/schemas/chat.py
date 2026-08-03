from pydantic import BaseModel

class chatRequest(BaseModel):
    session_id: str
    message: str

class sourceReference(BaseModel):
    filename: str
    start_line: int | None = None
    end_line: int | None = None

class chatResponse(BaseModel):
    answer: str
    source_references: list[sourceReference] | None = None