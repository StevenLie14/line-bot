from services import request_service
from linebot.v3.webhooks import MessageEvent, UserSource
from fastapi import APIRouter
from models.request.ticket import Ticket


router = APIRouter()

async def get_active_tickets(event: MessageEvent):
    return await request_service.get_active_tickets(event.source.group_id if not isinstance(event.source, UserSource) else None)


@router.post("/api/notify")
async def notify_new_ticket(ticket: Ticket):
    return await request_service.notify_new_ticket(ticket)
    
    
