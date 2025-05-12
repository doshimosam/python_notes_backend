import uuid

from pydantic import BaseModel


class NoteCreate(BaseModel):
    title: str
    content: str


class Note_all(BaseModel):
    id: uuid.UUID
    title: str
    content: str

    class Config:
        from_attributes = True
