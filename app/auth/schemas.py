from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr  # Automatic validation: rejects "hello", accepts "hello@gmail.com"
    password: str
    role: str = "student" #default

class UserPublic(BaseModel):
    id: int
    email: EmailStr
    role: str
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"