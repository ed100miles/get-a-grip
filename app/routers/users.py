from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import Session, select

from ..dependencies import get_session, oauth2_scheme
from ..mail import send_validation_email
from ..models import User, UserCreate, UserPublic
from ..settings import settings

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int
    sub: str
    exp: datetime | None = None


def create_access_token(data: TokenData, expires_delta: timedelta | None = None):
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode = data.model_copy(update={"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode.model_dump(), settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


@router.post("/create")
async def create_new_user(
    new_user: UserCreate,
    session: Session = Depends(get_session),
):
    db_user = User.model_validate(
        new_user, update={"hashed_password": pwd_context.hash(new_user.password)}
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    await send_validation_email(db_user)
    return {"message": "User created successfully - validate email to login"}


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
) -> Token:
    user = session.exec(
        select(User).where(User.username == form_data.username)
    ).one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="Unknown username")
    if not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=TokenData(sub=user.username, user_id=user.id),
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserPublic)
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str | None = payload.get("sub")
        if not username:
            raise ValueError("Invalid token payload")

        selected_user = session.exec(
            select(User).where(User.username == username)
        ).one_or_none()

        if not selected_user:
            raise ValueError("User not found")

        return selected_user

    except jwt.ExpiredSignatureError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        ) from err

    except jwt.InvalidTokenError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from err

    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(err),
            headers={"WWW-Authenticate": "Bearer"},
        ) from err
