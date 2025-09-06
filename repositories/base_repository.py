import json
import httpx

class BaseRepository:
    def __init__(self, base_url: str = "", headers: dict = None, verify: bool = True):
        self.base_url = base_url
        self.headers = headers or {}
        self.verify = verify
        self.client = httpx.AsyncClient(verify=self.verify)

    async def get(self, endpoint: str, headers: dict = None) -> dict:
        url = f"{self.base_url}{endpoint}"
        try:
            response = await self.client.get(url, headers={**self.headers, **(headers or {})})
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise ConnectionError(f"Failed to retrieve data from {url}") from e
        except json.JSONDecodeError as e:
            raise ValueError("Failed to parse an invalid JSON response from the server.") from e

    async def post(self, endpoint: str, data: dict, headers: dict = None) -> dict:
        url = f"{self.base_url}{endpoint}"
        try:
            response = await self.client.post(url, json=data, headers={**self.headers, **(headers or {})})
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise ConnectionError(f"Failed to retrieve data from {url}") from e
        except json.JSONDecodeError as e:
            raise ValueError("Failed to parse an invalid JSON response from the server.") from e

    async def close(self):
        await self.client.aclose()
