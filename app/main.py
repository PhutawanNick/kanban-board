from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine  
from .import models
from .routers import auth, tasks, boards, users


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Kanban Board API",
    description="API for managing Kanban boards, tasks, and users",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(boards.router)

@app.get("/")
def read_root():
    return {"message": "Kanban Running"}