from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup():
    return {"message": "User signup placeholder"}

@router.post("/login")
def login():
    return {"message": "User login placeholder"}