import aiohttp

from config import settings


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.auth = aiohttp.BasicAuth(settings.API_LOGIN, settings.API_PASSWORD)

    async def fetch_data(self, endpoint: str):
        async with aiohttp.ClientSession(auth=self.auth) as session:
            async with session.get(f'{self.base_url}/{endpoint}') as response:
                return await response.json()

    async def post_data(self, endpoint: str, data: dict):
        async with aiohttp.ClientSession(auth=self.auth) as session:
            async with session.post(f'{self.base_url}/{endpoint}', json=data) as response:
                return await response.json()
