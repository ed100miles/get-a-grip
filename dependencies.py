from sqlmodel import Session
from db_models import engine


def get_session():
    with Session(engine) as session:
        yield session
