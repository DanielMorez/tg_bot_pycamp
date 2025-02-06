import aiohttp


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def fetch_data(self, endpoint: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/{endpoint}") as response:
                return await response.json()
