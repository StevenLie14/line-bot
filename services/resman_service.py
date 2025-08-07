import httpx
from linebot.v3.messaging import TextMessageV2
from core.config import settings

async def request(url):
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(url)
        try:
            data = response.json()
            return data['data']
        except Exception as e:
            print("Failed to parse JSON:", e)
            return Exception(text=" Failed to retrieve data from RESMAN.")
        
async def get_assistant_semester_data(positions):
    return await request(f"{settings.RESMAN_URL}Assistant/AssistantSemesterData/Active?Position={";".join(positions)}")

