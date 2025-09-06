from core.config import settings
from utils.rest import get, post
from models.request.ticket import Ticket


async def get_active_request() -> list[Ticket]:
    try:
        raw_data = await get(f"{settings.REQUEST_SLC_URL}ticket",headers={"Authorization": f"Bearer {settings.REQUEST_SLC_TOKEN}"})
        all_tickets = [Ticket(**item) for item in raw_data['data']]
        return [ticket for ticket in all_tickets 
                if ticket.ticket_state.state_name not in ("Resolved","Wait Confirmation","Cancelled")]
    except (ConnectionError, ValueError) as e:
        print(f"An error occurred while getting the assistant semester data: {e}")
        raise e
    
