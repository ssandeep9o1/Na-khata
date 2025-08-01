from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class NoteBase(BaseModel):
    title: Optional[str] = None
    content: str

class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    content: Optional[str] = None

class Note(NoteBase):
    id: UUID
    shop_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True