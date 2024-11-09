from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str


@app.get("/data")
async def get_data():
    return {"message": "Hello, world!"}


@app.post("/data")
async def post_data(item: Item):
    return {"message": f"Received item with name {item.name} and description {item.description}"}
