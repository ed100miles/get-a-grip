import pytest
from fastapi.testclient import TestClient
from fastapi_mail import FastMail
from sqlmodel import Session, SQLModel, create_engine
from testcontainers.postgres import PostgresContainer

from app.dependencies import get_fast_mail, get_session
from app.main import app
from app.routers.users import TokenData, create_access_token
from app.seed_db import seed_db
from app.settings import mail_config


@pytest.fixture(scope="module")
def mock_seeded_db_engine():
    with PostgresContainer("postgis/postgis:16-3.4") as pg:
        engine = create_engine(pg.get_connection_url())
        SQLModel.metadata.create_all(engine)
        with Session(engine) as session:
            seed_db(session)
        yield engine


@pytest.fixture()
def mock_get_session(mock_seeded_db_engine):
    def _mock_session():
        with Session(mock_seeded_db_engine) as session:
            yield session
            session.rollback()
            session.close()

    return _mock_session


@pytest.fixture()
def mock_get_fast_mail():
    def _mock_fast_mail():
        mail_config.SUPPRESS_SEND = 1
        yield FastMail(mail_config)

    return _mock_fast_mail


@pytest.fixture()
def client(mock_get_session, mock_get_fast_mail):
    app.dependency_overrides[get_session] = mock_get_session
    app.dependency_overrides[get_fast_mail] = mock_get_fast_mail
    with TestClient(app) as client:
        yield client
    app.dependency_overrides = {}


@pytest.fixture(scope="module")
def test_user_token():
    return create_access_token(data=TokenData(sub="test", user_id=11, exp=None))
