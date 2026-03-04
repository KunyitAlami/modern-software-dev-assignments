from pydantic import BaseModel
from typing import List, Optional




class NoteCreate(BaseModel):
    content: str


class NoteResponse(BaseModel):
    id: int
    content: str
    created_at: str


class ActionItemResponse(BaseModel):
    id: int
    note_id: Optional[int]
    text: str
    done: int
    created_at: str


class ExtractRequest(BaseModel):
    text: str
    save_note: bool = False


class ActionItemCreateResponse(BaseModel):
    id: int
    text: str


class ExtractResponse(BaseModel):
    note_id: Optional[int]
    items: List[ActionItemCreateResponse]