from core.config import settings
from utils.rest import get, post
from models.request.ticket import Ticket


async def get_active_request() -> list[Ticket]:
    try:
        raw_data = await get(f"{settings.REQUEST_URL}ticket",headers={"Authorization": f"Bearer {settings.REQUEST_TOKEN}"})
        return [Ticket(**item) for item in raw_data['data']]
    except (ConnectionError, ValueError) as e:
        print(f"An error occurred while getting the assistant semester data: {e}")
        raise e
    
