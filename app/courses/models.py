from sqlmodel import SQLModel, Field
from typing import Optional

class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    
    title: str = Field(index=True)
    description: str
    instructor_id: int = Field(foreign_key="user.id")