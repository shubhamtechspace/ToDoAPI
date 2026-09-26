from fastapi import FastAPI, HTTPException, Depends
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.models.todo import Todo
from app.models.users import User
from app.routers.todo import router as todo_router
from app.routers.auth import router as auth_router


app = FastAPI()
app.include_router(todo_router, prefix="/todos", tags=["Todo"])
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Todo API is running"}


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "Todo API"
    }
