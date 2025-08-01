from sqlalchemy.orm import Session
from uuid import UUID

from app.api.v1 import models, schemas

def get_note(db: Session, note_id: UUID, shop_id: UUID) -> models.Note | None:
    """Gets a single note by ID, ensuring it belongs to the correct shop."""
    return db.query(models.Note).filter(models.Note.id == note_id, models.Note.shop_id == shop_id).first()

def get_notes_by_shop(db: Session, shop_id: UUID, skip: int = 0, limit: int = 100) -> list[models.Note]:
    """Gets a list of all notes for a given shop with pagination."""
    return db.query(models.Note).filter(models.Note.shop_id == shop_id).order_by(models.Note.created_at.desc()).offset(skip).limit(limit).all()

def create_note(db: Session, note: schemas.NoteCreate, shop_id: UUID) -> models.Note:
    """Creates a new note linked to a shop."""
    db_note = models.Note(**note.dict(), shop_id=shop_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def update_note(db: Session, db_note: models.Note, note_in: schemas.NoteUpdate) -> models.Note:
    """Updates a note's details."""
    update_data = note_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_note, key, value)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def delete_note(db: Session, db_note: models.Note):
    """Deletes a note."""
    db.delete(db_note)
    db.commit()
    return db_note