from fastapi import APIRouter, Depends, Header, HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session

from ..core import security
from ..db import session
from ..models import m_user
from ..schemas import user

router = APIRouter(tags=["Auth"])
blacklist = set()


@router.post("/register", status_code=status.HTTP_200_OK)
def user_register(request: user.user_get, db: Session = Depends(session.get_db)):
    new_user = m_user.User(
        username=request.username,
        email=request.email,
        password=security.get_password_hash(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/token", status_code=status.HTTP_200_OK)
def login(request: user.Login, db: Session = Depends(session.get_db)):
    user_e = db.query(m_user.User).filter(m_user.User.email == request.email).first()
    if not user_e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Email is not valid"
        )

    if not security.verified_password(request.password, user_e.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=("password is not valid")
        )
    return security.get_user_token(user=user_e)


@router.post("/refresh")
async def refresh_token(
    refresh_token: str = Header(...), db: Session = Depends(session.get_db)
):

    if refresh_token in blacklist:
        raise HTTPException(
            status_code=401, detail="Token is blacklisted. Please login again."
        )

    try:
        security.get_token_payload(refresh_token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return security.get_refresh_token(token=refresh_token, db=db)


@router.post("/logout")
async def logout(refresh_token: str):
    blacklist.add(refresh_token)
    return {"messege": "logout successfully"}
