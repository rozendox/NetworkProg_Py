import httpx
import asyncio

# URL base do servidor
BASE_URL = "http://127.0.0.1:8000"


async def create_item(item_id: int, name: str, description: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/items/",
                                     json={"id": item_id, "name": name, "description": description})
        print("Created item:", response.json())


async def get_all_items():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/items/")
        print("All items:", response.json())


async def get_item(item_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/items/{item_id}")
        print(f"Item {item_id}:", response.json())


async def update_item(item_id: int, name: str, description: str):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{BASE_URL}/items/{item_id}",
                                    json={"id": item_id, "name": name, "description": description})
        print("Updated item:", response.json())


async def delete_item(item_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/items/{item_id}")
        print("Delete response:", response.json())


# Executando as operações
async def main():
    await create_item(1, "Item 1", "A sample item")
    await get_all_items()
    await get_item(1)
    await update_item(1, "Updated Item 1", "An updated sample item")
    await get_item(1)
    await delete_item(1)
    await get_all_items()


# Rodar o cliente
asyncio.run(main())
