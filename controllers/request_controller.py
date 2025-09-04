from services import request_service, line_service
from linebot.v3.webhooks import MessageEvent, UserSource
from utils.helper import parse_user_args
from linebot.v3.messaging import TextMessageV2
from fastapi import APIRouter
from fastapi import Request, Header
from models.request.ticket import Ticket


async def get_active_tickets(event: MessageEvent):
    return await request_service.get_active_tickets(event.source.group_id if not isinstance(event.source, UserSource) else None)



router = APIRouter()


@router.post("/api/notify")
async def notify_new_ticket(ticket: Ticket):
    return await request_service.notify_new_ticket(ticket)
    
    
