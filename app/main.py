from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Todo API is running"}
