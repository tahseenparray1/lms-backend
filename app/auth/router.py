from app.auth.dependencies import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.core.db import get_session
from app.auth.models import User
from app.auth.schemas import UserCreate, UserPublic, UserLogin, Token
from app.core.security import get_password_hash , verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

# THE SIGNUP ENDPOINT
# response_model=UserPublic: This is the Magic Filter. It ensures we return ONLY
# the public data (id, email) and never the password, even if our code tries to.
@router.post("/signup", response_model=UserPublic)
def signup(user_data: UserCreate, session: Session = Depends(get_session)):
    
    statement = select(User).where(User.email == user_data.email)
    existing_user = session.exec(statement).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = get_password_hash(user_data.password)
    
    new_user = User(
        email=user_data.email,
        password_hash=hashed_pwd, 
        role=user_data.role
    )
    
    session.add(new_user)     
    session.commit()          
    session.refresh(new_user) 
    return new_user
@router.post("/login", response_model=Token)

def login(login_data: UserLogin, session: Session = Depends(get_session)):
    
    statement = select(User).where(User.email == login_data.email)
    user = session.exec(statement).first()
    
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    access_token = create_access_token(data={"sub": user.email})
    
    # 4. Return the Token
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=UserPublic)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user