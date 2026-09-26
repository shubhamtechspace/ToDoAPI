
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.security import get_current_user
from app.models.users import User
from app.database import get_db
from app.models.todo import Todo
from app.schemas.todo import TodoResponse, TodoCreate, TodoUpdate

router = APIRouter()


@router.get("/", response_model=list[TodoResponse], summary="Get all Todos", description="Retrieve the current user's todos with optional pagination.")
def get_todos(
    skip: int = 0,
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(Todo)
        .filter(Todo.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{todo_id}", response_model=TodoResponse, responses={
    404: {"description": "Todo not found"}
}, summary="Get a specific todo", description="Retrieve a specific todo owned by the current user.")
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    todo = db.query(Todo) .filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()

    if todo is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    return todo


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED, summary="Create a new todo", description="Create a new todo in the database.")
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_todo = Todo(
        title=todo.title,
        description=todo.description,
        completed=False,
        user_id=current_user.id
    )

    try:

        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)

    except Exception:
        db.rollback()
    raise

    return new_todo


@router.put("/{todo_id}", response_model=TodoResponse, responses={
    404: {"description": "Todo not found"}
}, summary="Replace a todo", description="Update a todo owned by the current user.")
def update_todo(
    todo_id: int,
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()

    if existing_todo is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    existing_todo.title = todo.title
    existing_todo.description = todo.description

    try:
        db.commit()
        db.refresh(existing_todo)

    except Exception:
        db.rollback()
        raise

    return existing_todo


@router.patch("/{todo_id}", response_model=TodoResponse, responses={
    404: {"description": "Todo not found"}
}, summary="Partially update a todo", description="Update complete todo based on the todo id.")
def patch_todo(
    todo_id: int,
    todo: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_todo = db.query(Todo) .filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()

    if existing_todo is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    update_data = todo.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(existing_todo, field, value)

    try:
        db.commit()
        db.refresh(existing_todo)

    except Exception:
        db.rollback()
        raise

    return existing_todo


@router.delete("/{todo_id}",  status_code=status.HTTP_204_NO_CONTENT, responses={
    404: {"description": "Todo not found"}
}, summary="Delete a todo", description="Delete a todo based on todo id.")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_todo = db.query(Todo) .filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()

    if existing_todo is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    try:
        db.delete(existing_todo)
        db.commit()

    except Exception:
        db.rollback()
        raise
