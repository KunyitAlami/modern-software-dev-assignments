from datetime import datetime
from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)


class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotePatch(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    content: str | None = Field(None, min_length=1)

class ActionItemCreate(BaseModel):
    description: str = Field(..., min_length=1, max_length=500)
    note_id: int | None = None  # optional relationship


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool
    note_id: int | None  # expose relationship
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ActionItemPatch(BaseModel):
    description: str | None = Field(None, min_length=1, max_length=500)
    completed: bool | None = None
    note_id: int | None = None  # allow updating relationship