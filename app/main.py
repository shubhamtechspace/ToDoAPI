from fastapi import FastAPI, HTTPException, Depends
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.models.todo import Todo
from app.routers.todo import router as todo_router


app = FastAPI()
app.include_router(todo_router, prefix="/todos")
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
