import asyncio
import time
from datetime import datetime

from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False


def test_item_with_error_message():
    item = Item(name="test", price="hi")
    print(item)
    assert item.name == "test"
    assert item.price == 10.0
    assert item.is_offer is False


def test_item_with_no_error_message():
    item = Item(name="test", price=10)
    print(item)
    assert item.name == "test"
    assert item.price == 10.0
    assert item.is_offer is False


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


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


@app.post("/items/")
def create_item(item: Item):
    return {"message": "Item created", "item": item}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"message": "Item updated", "item_id": item_id, "new_values": item}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": "Item deleted", "item_id": item_id}


@app.post("/async-endpoint")
async def read_async():
    await asyncio.sleep(2)  # Simulate an async operation
    return {"status": f"This endpoint waited for 2 seconds asynchronously: {datetime.now()}"}


def send_notification(email: str, message: str):
    # Logic to send email/notification
    print(f"Sending notification to {email} with message: {message} - {datetime.now()}")


@app.post("/notify")
def notify_user(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_notification, email, "Your data is processed")
    return {"message": f"Notification scheduled: {datetime.now()}"}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response: Response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/health")
def health_check():
    return {"status": "ok", "time": datetime.now()}


# To run the server:
# uvicorn main:app --reload

# run with main
if __name__ == "__main__":
    test_item_with_no_error_message()
    test_item_with_error_message()
