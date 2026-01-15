from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.db.base import Base, engine
from app.routers import organizations

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Organization Directory API",
    description="REST API for managing organizations, buildings, and activities",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    organizations.router
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
