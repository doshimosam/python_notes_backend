from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core import security
from ..core.security import token_auth_scheme
from ..db import session
from ..models import m_user
from ..schemas import user

router = APIRouter(
    tags=["user"], prefix="/user", dependencies={Depends(token_auth_scheme)}
)


@router.get("/me", response_model=user.UserOut, status_code=status.HTTP_200_OK)
def get_profile(
    email: str = Depends(security.verify_token), db: Session = Depends(session.get_db)
):
    user = db.query(m_user.User).filter(m_user.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{me}")
def up_user(
    me,
    request: user.Change_profile,
    db: Session = Depends(session.get_db),
    current_user: m_user.User = Depends(security.get_current_user),
):
    update_user = db.query(m_user.User).filter(m_user.User.email == me)
    if not update_user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with email {me} not found",
        )
    update_user.update(request.dict())
    db.commit()
    return {"detail": "successfully updated"}


@router.post("/change-password")
def change_password(
    new_password: str,
    db: Session = Depends(session.get_db),
    current_user: m_user.User = Depends(security.get_current_user),
):
    hashed_pw = security.get_password_hash(new_password)
    current_user.password = hashed_pw
    db.commit()
    return {"message": "Password updated successfully"}
