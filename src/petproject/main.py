from typing import List, Union
from uuid import UUID, uuid4

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="App")

item_values = []


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/nodes/{id}")
def update_item(id: str):
    pass


# @app.get("/items", response_model=List[Item])
# def get_all_items():
#     return item_values


# @app.get("/item", response_model=List[Item])
# def read_item(item_id: UUID):
#     current_item = list(filter(lambda user: user.item_id == item_id, item_values))
#     return current_item
