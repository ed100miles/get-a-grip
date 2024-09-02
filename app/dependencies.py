from sqlmodel import Session
from app.db_models import engine


def get_session():
    with Session(engine) as session:
        yield session
