from services import request_service
from linebot.v3.webhooks import MessageEvent, UserSource
from utils.helper import parse_user_args
from linebot.v3.messaging import TextMessageV2


async def get_active_tickets(event: MessageEvent):
    return await request_service.get_active_tickets(event.source.group_id if not isinstance(event.source, UserSource) else None)