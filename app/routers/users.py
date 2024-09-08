import json
from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_mail import FastMail, MessageSchema, MessageType
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature, SignatureExpired
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import Session, select

from ..constants import datetime_format
from ..dependencies import get_fast_mail, get_session, oauth2_scheme
from ..models import User, UserCreate, UserPublic
from ..settings import settings

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

serializer = URLSafeTimedSerializer(settings.SECRET_KEY)


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


def create_url_safe_token(data: UserPublic) -> str:
    return serializer.dumps(data.model_dump_json())


def decode_url_safe_token(token: str) -> UserPublic:
    try:
        decoded_token = serializer.loads(
            token, max_age=settings.VALIDATION_EMAIL_EXPIRE_MINUTES * 60
        )
    except SignatureExpired as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Too slow! Token expired."
        ) from err
    except BadSignature as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Uuhhh, this has been tampered with, the police have been called.",
        ) from err
    token_data = json.loads(decoded_token)
    return UserPublic(
        username=token_data["username"],
        email=token_data["email"],
        id=int(token_data["id"]),
        created_at=datetime.strptime(token_data["created_at"], datetime_format),
    )


async def send_validation_email(mail: FastMail, user: User, subject: str, html: str):
    message = MessageSchema(
        subject=subject,
        recipients=[user.email],
        body=html,
        subtype=MessageType.html,
    )
    await mail.send_message(message)


@router.post("/create")
async def create_new_user(
    new_user: UserCreate,
    session: Session = Depends(get_session),
    fast_mail: FastMail = Depends(get_fast_mail),
):
    db_user = User.model_validate(
        new_user, update={"hashed_password": pwd_context.hash(new_user.password)}
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    public_user = UserPublic.model_validate(
        db_user
    )  # dont want to include hashed password in token just in case!
    token = create_url_safe_token(public_user)
    link = f"{settings.DOMAIN}/user/validate/{token}"
    email_html = f"""
    <h1>Get A Grip - Validate your email</h1>
    <p>Click the link below to validate your email and get started with Get A Grip</p>
    <p>
    You have {settings.VALIDATION_EMAIL_EXPIRE_MINUTES} minutes to validate your email
    </p>
    <a href="{link}">Validate Email</a>
    """
    await send_validation_email(
        fast_mail, db_user, "Get A Grip - Validate your email", email_html
    )
    return {
        "message": "User created successfully - validate email to login",
        "minutes_to_validate": settings.VALIDATION_EMAIL_EXPIRE_MINUTES,
    }


@router.get("/validate/{token}")
async def validate_email(token: str, session: Session = Depends(get_session)):
    token_user = decode_url_safe_token(token)
    statement = select(User).where(User.id == token_user.id)
    db_user = session.exec(statement).one()
    db_user.email_validated = True
    session.add(db_user)
    session.commit()
    return {"message": "Email validated successfully"}


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
