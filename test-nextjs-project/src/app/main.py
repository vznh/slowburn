# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import random

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str

class Item(BaseModel):
    id: int
    name: str
    price: float

users = [
    User(id=1, name="Alice", email="alice@example.com"),
    User(id=2, name="Bob", email="bob@example.com"),
]

items = [
    Item(id=1, name="Laptop", price=999.99),
    Item(id=2, name="Phone", price=499.99),
]

@app.get("/users", response_model=List[User])
async def get_users():
    # BUG: This endpoint will randomly fail
    if random.random() < 0.5:
        raise HTTPException(status_code=500, detail="Random server error")
    return users

@app.get("/items", response_model=List[Item])
async def get_items():
    # BUG: This endpoint will return items with incorrect types
    return [{"id": "not_an_int", "name": item.name, "price": str(item.price)} for item in items]

@app.post("/process")
async def process_data(data: dict):
    # BUG: This endpoint doesn't properly handle missing keys
    result = data['value1'] + data['value2']
    return {"result": result}

@app.get("/user/{user_id}")
async def get_user(user_id: int):
    # BUG: This endpoint doesn't properly handle non-existent users
    user = next((u for u in users if u.id == user_id), None)
    return user

@app.put("/item/{item_id}")
async def update_item(item_id: int, item: Item):
    # BUG: This endpoint updates the wrong item
    for i, existing_item in enumerate(items):
        if existing_item.id == item_id + 1:  # Intentional off-by-one error
            items[i] = item
            return {"message": "Item updated successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)