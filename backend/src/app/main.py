from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import engine, Base
from app import models
from app.routes import admin_router, transcript_router, skills_router, parent_skills_router, quiz_router

app = FastAPI(title="Transcript Skill Validation API")

# Create database tables
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(admin_router)
app.include_router(transcript_router)
app.include_router(skills_router)
app.include_router(parent_skills_router)
app.include_router(quiz_router)

@app.get("/health")
def health():
    return {"status": "ok"}
