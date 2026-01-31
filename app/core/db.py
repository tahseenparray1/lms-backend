from sqlmodel import SQLModel, create_engine, Session
from fastapi import Depends
from typing import Annotated

DATABASE_URL = "postgresql://lms_user:lms_password@localhost:5432/lms_db"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]