from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.api.api import api_router
from app.core.config import API_V1_STR
from app.db.init_db import init_db
from app.db.session import get_db

app = FastAPI(
    title="FastAPI PostgreSQL Service",
    description="API service with JWT authentication and PostgreSQL integration",
    version="1.0.0",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=API_V1_STR)

@app.on_event("startup")
def startup_event():
    db = next(get_db())
    init_db(db)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI PostgreSQL Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)