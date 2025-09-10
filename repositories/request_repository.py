from core import settings
from models.request import Ticket
from . import BaseRepository

class RequestRepository(BaseRepository):
    def __init__(self):
        super().__init__(
            base_url=settings.REQUEST_SLC_URL,
            headers={"Authorization": f"Bearer {settings.REQUEST_SLC_TOKEN}"},
            verify=False
        )

    async def get_active_request(self) -> list[Ticket]:
        try:
            raw_data = await self.get("/ticket")
            all_tickets = [Ticket(**item) for item in raw_data["data"]]
            return [
                ticket for ticket in all_tickets
                if ticket.ticket_state.state_name not in ("Resolved", "Wait Confirmation", "Cancelled")
            ]
        except Exception as e:
            print(f"An error occurred while getting active requests: {e}")
            raise e
