from fastapi import APIRouter
from models.request.ticket import Ticket
from services import RequestService
from linebot.v3.webhooks import MessageEvent, UserSource
from . import BaseController

class RequestController(BaseController):
    def __init__(self, request_service: RequestService):
        super().__init__()
        self.router = APIRouter()
        self.router.post("/api/notify")(self.notify_new_ticket)
        self.request_service = request_service
        self.line_routes = {
            "/tickets" : self.get_active_tickets
        }

    async def get_active_tickets(self, event: MessageEvent):
        return await self.request_service.get_active_tickets(
            event.source.group_id if not isinstance(event.source, UserSource) else None
        )

    async def notify_new_ticket(self, ticket: Ticket):
        return await self.request_service.notify_new_ticket(ticket)
