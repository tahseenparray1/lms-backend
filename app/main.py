from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.courses.router import router as courses_router

app = FastAPI(title="Scalable LMS API")

app.include_router(auth_router)
app.include_router(courses_router)

@app.get("/")
def health_check():
    return {"status": "ok", "system": "LMS Backend"}