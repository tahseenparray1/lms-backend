from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlmodel import Session, select
from app.core.db import get_session
from app.auth.models import User
from app.core.security import SECRET_KEY, ALGORITHM

security = HTTPBearer()


def get_current_user(
    token_creds: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    
    token = token_creds.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. Decode the Token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
        
    # 2. Find the User in DB
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    
    if user is None:
        raise credentials_exception
        
    return user