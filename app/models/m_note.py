import uuid

from sqlalchemy import UUID, Column, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import relationship

from ..db.base import Base


class Note(Base):
    __tablename__ = "Note"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    creator = relationship("User", back_populates="Notes")
