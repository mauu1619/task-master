from sqlmodel import SQLModel

from app import models
from .session import engine


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == '__main__':
    create_db_and_tables()