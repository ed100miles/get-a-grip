from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from settings import settings

from ..dependencies import get_session, oauth2_scheme
from ..models import Pinch, PinchCreate

router = APIRouter(prefix="/pinch")


@router.post("/create", response_model=Pinch)
async def create_new_pinch(
    new_pinch: PinchCreate,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=400, detail="Invalid token - no user_id")
    db_pinch = Pinch.model_validate(new_pinch, update={"user_id": user_id})
    session.add(db_pinch)
    session.commit()
    session.refresh(db_pinch)
    return db_pinch
