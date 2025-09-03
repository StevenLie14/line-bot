import json
import httpx

async def get(url: str, headers=None) -> dict:
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url,headers=headers)
            response.raise_for_status()
            return response.json()
            
    except httpx.RequestError as e:
        raise ConnectionError(f"Failed to retrieve data from {url}") from e
        
    except json.JSONDecodeError as e:
        raise ValueError("Failed to parse an invalid JSON response from the server.") from e
            
async def post(url, data,headers=None):
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(url, json=data,headers=headers)
            response.raise_for_status()
            return response.json()
            
    except httpx.RequestError as e:
        raise ConnectionError(f"Failed to retrieve data from {url}") from e
        
    except json.JSONDecodeError as e:
        raise ValueError("Failed to parse an invalid JSON response from the server.") from e