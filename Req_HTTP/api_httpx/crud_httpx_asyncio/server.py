from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


# Modelo do Item
class Item(BaseModel):
    id: int
    name: str
    description: str = "No description provided"


# Banco de dados simulado
items_db = {}


# Endpoint para criar um novo item
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    if item.id in items_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    items_db[item.id] = item
    return item


# Endpoint para ler todos os itens
@app.get("/items/", response_model=List[Item])
async def read_items():
    return list(items_db.values())


# Endpoint para ler um item específico
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    item = items_db.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# Endpoint para atualizar um item
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item
    return item


# Endpoint para deletar um item
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": "Item deleted successfully"}
