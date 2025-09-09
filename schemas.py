from pydantic import BaseModel
from datetime import datetime

class MemoryCreate(BaseModel):
    content: str

class MemorySearch(BaseModel):
    query: str


class MemoryResponse(BaseModel):
    id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True # ✅ Pydantic v2 replacement for orm_mode
