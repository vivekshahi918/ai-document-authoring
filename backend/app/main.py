# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Import both routers
from .api.v1.endpoints import auth, projects, sections
from .db import init_db

app = FastAPI(title="AI Document Authoring Platform API")

@app.on_event("startup")
async def on_startup():
    await init_db()

# Define the list of allowed origins (URLs)
origins = [
    "https://ai-document-authoring.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)

# Include both routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(sections.router, prefix="/api/v1/sections", tags=["Sections"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Document Authoring Platform!"}