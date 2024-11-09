import httpx


async def get_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://127.0.0.1:8000/data")
        print(response.json())


# Para rodar o cliente
import asyncio

asyncio.run(get_data())
