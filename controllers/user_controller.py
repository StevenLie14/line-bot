from services import user_service
from core.constant import Position
from sqlalchemy.orm import Session
from linebot.v3.webhooks import MessageEvent
from core.config import settings
from linebot.v3.messaging import TextMessageV2


async def get_active_rnd():
    return await user_service.get_user_by_positions(Position.RND)

async def get_active_dba():
    return await user_service.get_user_by_positions(Position.DBA)

async def get_active_na():
    return await user_service.get_user_by_positions(Position.KMG_NA)

async def get_active_op():
    return await user_service.get_user_by_positions(Position.OP)

async def get_active_part():
    return await user_service.get_user_by_positions(Position.PART)

async def get_active_resman():
    return await user_service.get_user_by_positions(Position.RESMAN)

async def get_active_head():
    return await user_service.get_user_by_positions(Position.HEAD)

async def sync_line_id(event: MessageEvent, token: str, initial: str):
    if (token != settings.SYNC_TOKEN):
        return TextMessageV2(text="Invalid sync token.")

    line_id = event.source.user_id
    await user_service.sync_line_id(initial, line_id)
    return TextMessageV2(text=f"Synced {initial} to {line_id}")