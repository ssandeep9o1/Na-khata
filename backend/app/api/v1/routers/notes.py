from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.api.v1 import schemas
from app.api.v1.crud import crud_note
from app.core.database import get_db
from app.api.v1.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Note, status_code=status.HTTP_201_CREATED)
def create_note(
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new note for the authenticated user's shop."""
    shop_id = UUID(current_user.get("sub"))
    return crud_note.create_note(db=db, note=note, shop_id=shop_id)

@router.get("/", response_model=List[schemas.Note])
def read_notes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Retrieve all notes for the authenticated user's shop."""
    shop_id = UUID(current_user.get("sub"))
    notes = crud_note.get_notes_by_shop(db, shop_id=shop_id, skip=skip, limit=limit)
    return notes

@router.get("/{note_id}", response_model=schemas.Note)
def read_note(
    note_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Retrieve a specific note by ID."""
    shop_id = UUID(current_user.get("sub"))
    db_note = crud_note.get_note(db, note_id=note_id, shop_id=shop_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

@router.put("/{note_id}", response_model=schemas.Note)
def update_note(
    note_id: UUID,
    note_in: schemas.NoteUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update a note's details."""
    shop_id = UUID(current_user.get("sub"))
    db_note = crud_note.get_note(db, note_id=note_id, shop_id=shop_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return crud_note.update_note(db=db, db_note=db_note, note_in=note_in)

@router.delete("/{note_id}", response_model=schemas.Note)
def delete_note(
    note_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete a note."""
    shop_id = UUID(current_user.get("sub"))
    db_note = crud_note.get_note(db, note_id=note_id, shop_id=shop_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return crud_note.delete_note(db=db, db_note=db_note)