import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from testcontainers.postgres import PostgresContainer

from app.dependencies import get_session
from app.main import app
from app.routers.users import TokenData, create_access_token
from app.seed_db import seed_db


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
def client(mock_get_session):
    app.dependency_overrides[get_session] = mock_get_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides = {}


@pytest.fixture(scope="module")
def test_user_token():
    return create_access_token(data=TokenData(sub="test", user_id=11, exp=None))
