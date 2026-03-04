from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.utils.responses import success

from ..db import get_db
from ..models import Note
from ..schemas import NoteCreate, NoteRead, SuccessResponse

router = APIRouter(prefix="/notes", tags=["notes"])


# @router.get("/", response_model=SuccessResponse[dict])
# def list_notes(db: Session = Depends(get_db)) ->  SuccessResponse[list[NoteRead]]:
#     rows = db.execute(select(Note)).scalars().all()
#     return success([NoteRead.model_validate(row) for row in rows])


@router.get("/", response_model=SuccessResponse[dict])
def list_notes(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
) -> SuccessResponse[dict]:

    total = db.execute(select(Note)).scalars().all()
    total_count = len(total)

    rows = db.execute(select(Note).offset((page - 1) * page_size).limit(page_size)).scalars().all()

    items = [NoteRead.model_validate(row) for row in rows]

    return success(
        {
            "items": items,
            "total": total_count,
            "page": page,
            "page_size": page_size,
        }
    )


@router.post("/", response_model=SuccessResponse[NoteRead], status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> SuccessResponse[NoteRead]:
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.flush()
    db.refresh(note)
    return success(NoteRead.model_validate(note))


@router.get("/search/", response_model=SuccessResponse[list[NoteRead]])
def search_notes(
    q: Optional[str] = None, db: Session = Depends(get_db)
) -> SuccessResponse[list[NoteRead]]:
    if not q:
        rows = db.execute(select(Note)).scalars().all()
    else:
        rows = (
            db.execute(select(Note).where((Note.title.contains(q)) | (Note.content.contains(q))))
            .scalars()
            .all()
        )
    return success([NoteRead.model_validate(row) for row in rows])


@router.get("/{note_id}", response_model=SuccessResponse[NoteRead])
def get_note(note_id: int, db: Session = Depends(get_db)) -> SuccessResponse[NoteRead]:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return success(NoteRead.model_validate(note))
