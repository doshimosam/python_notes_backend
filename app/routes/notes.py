from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core import security
from ..db import session
from ..models import m_note, m_user
from ..schemas import note

router = APIRouter(
    tags=["Note"],
    prefix="/notes",
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[note.Note_all])
def get_all_notes(
    db: Session = Depends(session.get_db),
    current_user: m_user.User = Depends(security.get_current_user),
):
    all_notes = (
        db.query(m_note.Note).filter(current_user.id == m_note.Note.user_id).all()
    )
    return all_notes


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=note.NoteCreate)
def create_note(
    request: note.NoteCreate,
    db: Session = Depends(session.get_db),
    current_user: m_user.User = Depends(security.get_current_user),
):
    new_note = m_note.Note(
        title=request.title, content=request.content, user_id=current_user.id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=note.NoteCreate)
def get_note_with_id(
    id,
    db: Session = Depends(session.get_db),
    current_user: m_user.User = Depends(security.get_current_user),
):
    note_instance = db.query(m_note.Note).filter(id == m_note.Note.id).first()
    if not note_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with id {id} not found"
        )
    return note_instance


@router.put("/{id}", status_code=status.HTTP_200_OK)
def update_note(
    id: str,
    request: note.NoteCreate,
    db: Session = Depends(session.get_db),
    current_user: m_user.User = Depends(security.get_current_user),
):
    note_query = db.query(m_note.Note).filter(m_note.Note.id == id)
    if not note_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with id {id} not found"
        )
    note_query.update(request.dict())
    db.commit()
    return {"message": "Note updated successfully"}


@router.delete("/{id}")
def delete_note(
    id: str,
    db: Session = Depends(session.get_db),
    current_user: m_user.User = Depends(security.get_current_user),
):
    note_query = db.query(m_note.Note).filter(m_note.Note.id == id)
    if not note_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with id {id} not found"
        )
    note_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Note deleted successfully"}
