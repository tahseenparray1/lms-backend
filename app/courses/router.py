from fastapi import APIRouter

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/")
def get_courses():
    return [{"id": 1, "title": "FastAPI for Beginners"}]

@router.post("/")
def create_course():
    return {"message": "Course created"}