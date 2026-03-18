from sqlmodel import create_engine, Session

from app.core.config import CONNECTION_STR


engine = create_engine(CONNECTION_STR)

def get_session():
    with Session(engine) as session:
        yield session