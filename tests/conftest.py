import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session, StaticPool

from app import models
from app.main import app
from app.db.session import get_session
from app.core.security import create_access_token


sqlite_url = "sqlite:///:memory:"
engine = create_engine(
    sqlite_url, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)


@pytest.fixture
def session():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def client(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(session: Session):
    from app.models.user import User
    from app.core.security import get_password_hash

    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password=get_password_hash("testuser123")
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def user_token(test_user):
    return create_access_token({"sub": test_user.username})


@pytest.fixture
def test_project(session: Session, test_user):
    from app.models.project import Project

    project = Project(
        title="testproject",
        description="testproject1",
        owner_id=test_user.id
    )

    session.add(project)
    session.commit()
    session.refresh(project)
    return project