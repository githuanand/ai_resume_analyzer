from fastapi import FastAPI

from routers.resume import router as resume_router
from routers.jobs import router as jobs_router
from routers.auth import router as auth_router
from routers.improve_resume import router as improve_resume_router


from services.redis_service import test_redis


from database.db import engine
from database.models import Base

app = FastAPI(
    title="AI Resume SaaS",
    description="AI-Powered Resume Analysis and Job Matching Platform",
    version="1.0.0"
)

# Create PostgreSQL tables automatically
Base.metadata.create_all(bind=engine)

# Auth Routes
app.include_router(
    auth_router,
    tags=["Authentication"]
)

# Resume Routes
app.include_router(
    resume_router,
    tags=["Resume"]
)

# Job Matching Routes
app.include_router(
    jobs_router,
    tags=["Job Matching"]
)

# Resume Improvement Routes
app.include_router(
    improve_resume_router,
    tags=["Resume Improvement"]
)


@app.get("/")
def home():

    return {
        "message": "AI Resume SaaS Running",
        "version": "1.0.0",
        "status": "active"
    }
    
@app.get("/redis-test")
def redis_test():

    return {
        "redis_value": test_redis()
    }