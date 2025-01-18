from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": f"Hello World: {datetime.now()}"}
    # return {"message": "Hello World"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

@app.get("/items/")
def read_items(page: int = 1, limit: int = 10):
    return {"page": page, "limit": limit}

# To run the server:
# uvicorn main:app --reload
# uvicorn main:app --reload