from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Todo API is running"}


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "Todo API"
    }


@app.get("/todos")
def get_todos():
    return [
        {
            "id": 1,
            "title": "Learn FastAPI",
            "completed": False
        },
        {
            "id": 2,
            "title": "Build To-Do API",
            "completed": False
        }
    ]
