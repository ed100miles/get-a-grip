from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from app.db_models import engine

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


def get_session():
    with Session(engine) as session:
        yield session
