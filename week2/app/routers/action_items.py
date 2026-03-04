from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException

from .. import db
from ..schemas import ExtractRequest, ExtractResponse, ActionItemResponse
from ..services.extract import extract_action_items, extract_action_items_llm


router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=ExtractResponse)
def extract(payload: ExtractRequest) -> ExtractResponse:
    """
    Extract action items using heuristic extraction.
    """

    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    note_id: Optional[int] = None
    if payload.save_note:
        note_id = db.insert_note(text)

    items = extract_action_items(text)
    ids = db.insert_action_items(items, note_id=note_id)

    return ExtractResponse(
        note_id=note_id,
        items=[{"id": i, "text": t} for i, t in zip(ids, items)],
    )


@router.post("/extract-llm", response_model=ExtractResponse)
def extract_llm(payload: ExtractRequest) -> ExtractResponse:
    """
    Extract action items using LLM-powered extraction.
    """

    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    note_id: Optional[int] = None
    if payload.save_note:
        note_id = db.insert_note(text)

    items = extract_action_items_llm(text)
    ids = db.insert_action_items(items, note_id=note_id)

    return ExtractResponse(
        note_id=note_id,
        items=[{"id": i, "text": t} for i, t in zip(ids, items)],
    )


@router.get("", response_model=List[ActionItemResponse])
def list_all(note_id: Optional[int] = None) -> List[ActionItemResponse]:
    """
    List all stored action items (optionally filtered by note_id).
    """

    rows = db.list_action_items(note_id=note_id)

    return [
        ActionItemResponse(
            id=r["id"],
            note_id=r["note_id"],
            text=r["text"],
            done=bool(r["done"]),
            created_at=r["created_at"],
        )
        for r in rows
    ]


@router.post("/{action_item_id}/done")
def mark_done(action_item_id: int, done: bool = True) -> dict:
    """
    Mark an action item as done/undone.
    """
    db.mark_action_item_done(action_item_id, done)
    return {"id": action_item_id, "done": done}
