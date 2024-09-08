from fastapi.security import OAuth2PasswordBearer
from fastapi_mail import FastMail
from sqlmodel import Session

from .models import engine
from .settings import mail_config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


def get_fast_mail():
    fast_mail = FastMail(mail_config)
    yield fast_mail


def get_session():
    with Session(engine) as session:
        yield session
        session.close()
