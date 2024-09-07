import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from testcontainers.postgres import PostgresContainer

from app.dependencies import get_session
from app.main import app
from app.seed_db import seed_db


@pytest.fixture(scope="module")
def mock_engine():
    with PostgresContainer("postgis/postgis:16-3.4") as pg:
        engine = create_engine(pg.get_connection_url())
        yield engine


@pytest.fixture(scope="module")
def mock_get_session(mock_engine):
    def _mock_session():
        SQLModel.metadata.create_all(mock_engine)
        with Session(mock_engine) as session:
            seed_db(session)
            yield session
            session.rollback()
            session.close()

    return _mock_session


@pytest.fixture(scope="module")
def client(mock_get_session):
    app.dependency_overrides[get_session] = mock_get_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides = {}
