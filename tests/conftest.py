import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session, StaticPool

from app.main import app
from app.db.session import get_session


sqlite_url = "sqlite://"
engine = create_engine(
    sqlite_url, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()