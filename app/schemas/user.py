import datetime
import uuid

from pydantic import BaseModel


class user_get(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class Login(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


class Change_profile(BaseModel):
    username: str
    email: str


class Change_password(BaseModel):
    password: str

    class Config:
        from_attributes = True
