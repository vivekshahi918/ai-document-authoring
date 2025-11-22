# backend/app/main.py - FINAL CORRECTED VERSION

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.endpoints import auth, projects, sections
from .db import init_db
from .core.config import settings  

if not settings.GEMINI_API_KEY:
    raise ValueError(
        "FATAL ERROR: GEMINI_API_KEY is not set in the environment variables. "
        "Please check that you have a .env file in the 'backend' folder and that it contains the key."
    )


app = FastAPI(title="AI Document Authoring Platform API")

@app.on_event("startup")
async def on_startup():
    await init_db()

origins = [
    # "http://localhost:3000",
    "https://ai-document-authoring.vercel.app" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(sections.router, prefix="/api/v1/sections", tags=["Sections"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Document Authoring Platform!"}