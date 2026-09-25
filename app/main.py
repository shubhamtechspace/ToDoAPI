from fastapi import FastAPI, HTTPException
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate

app = FastAPI()

todos = []


@app.get("/")
def root():
    return {"message": "Todo API is running"}


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "Todo API"
    }


@app.get("/todos", response_model=list[TodoResponse])
def get_totos():
    return todos


@app.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate):
    new_todo = {
        "id": len(todos)+1,
        "title": todo["title"],
        "description": todo.get("description"),
        "completed": False
    }
    todos.append(new_todo)
    return new_todo


@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )


@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todos(todo_id: int, todo: TodoCreate):
    for existing_todo in todos:
        if existing_todo["id"] == todo_id:
            existing_todo["title"] == todo["title"]
            existing_todo["description"] = todo.get("description")
            existing_todo["completed"] = todo.get("completed", False)

            return existing_todo
    raise HTTPException(
        status_code=404,
        detail="Todo not Found"
    )


@app.patch("/todos/{todo_id}", response_model=TodoResponse)
def patch_todo(todo_id: int, todo: TodoUpdate):
    for existing_todo in todos:
        if existing_todo["id"] == todo_id:

            if "title" in todo:
                existing_todo["title"] = todo["title"]

            if "description" in todo:
                existing_todo["description"] = todo["description"]

            if "completed" in todo:
                existing_todo["completed"] = todo["completed"]

            return existing_todo

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )


@app.delete("/todos/{todo_id}", response_model=TodoResponse)
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo["id"] == todo_id:
            deleted_todo = todos.pop(index)
            return deleted_todo

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )
