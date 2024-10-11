from sqlmodel import create_engine, Session, SQLModel
from collections.abc import Generator
from typing import Annotated
from fastapi import Depends
import os

PROJECT_ROOT: str = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
BASE_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
database_url = f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}"
engine = create_engine(database_url)
SQLModel.metadata.create_all(engine)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]  # 别名，简化依赖关系的声明
