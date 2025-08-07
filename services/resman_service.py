import httpx
from linebot.v3.messaging import TextMessageV2
from core.config import settings
from typing import List, Optional
from models.resman.assistant_semester_data import AssistantSemesterData
from models.resman.assistant_shift import AssistantShift

async def request(url):
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(url)
        try:
            data = response.json()
            return data
        except Exception as e:
            print("Failed to parse JSON:", e)
            return Exception(text=" Failed to retrieve data from RESMAN.")
        
async def get_assistant_semester_data(positions: list[str]) -> list[AssistantSemesterData]:
    raw_data = await request(f"{settings.RESMAN_URL}Assistant/AssistantSemesterData/Active?Position={';'.join(positions)}")

    if isinstance(raw_data, Exception):
        raise raw_data

    return [AssistantSemesterData(**item) for item in raw_data['data']]

async def get_assistant_shift(initial: str):
    raw_data = await request(f"{settings.RESMAN_URL}Assistant/Shifts?Initial={initial}")

    if isinstance(raw_data, Exception):
        raise raw_data

    return [AssistantShift(**item) for item in raw_data['shifts']]

