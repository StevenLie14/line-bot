from fastapi import APIRouter
from models.request.ticket import Ticket
from services import RequestService
from linebot.v3.webhooks import MessageEvent, UserSource
from . import BaseController
from linebot.v3.messaging import TextMessageV2
from core import settings

class RequestController(BaseController):
    def __init__(self, request_service: RequestService):
        super().__init__()
        self.router = APIRouter()
        self.router.post("/api/notify")(self.notify_new_ticket)
        self.request_service = request_service
        self.line_routes = {
            "/tickets": {
                "handler": self.get_active_tickets,
                "description": "Show all active tickets in RnDBA group. Usage: /tickets",
                "active" : True,
            }
}

    async def get_active_tickets(self, event: MessageEvent):
        if isinstance(event.source, UserSource) and event.source.group_id is None :
            return TextMessageV2(text="You must be in a group to use this command.")
        
        if event.source.group_id != settings.RNDBA_GROUP_ID:
            return TextMessageV2(text="You must be in the RnDBA group to use this command.")
        
        return await self.request_service.get_active_tickets(
            event.source.group_id
        )

    async def notify_new_ticket(self, ticket: Ticket):
        return await self.request_service.notify_new_ticket(ticket)
