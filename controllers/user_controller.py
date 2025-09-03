from services import user_service
from core.constant import Position
from linebot.v3.webhooks import MessageEvent, UserSource
from core.config import settings
from linebot.v3.messaging import TextMessageV2
from utils.helper import parse_user_args


async def get_active_rnd(event : MessageEvent):
    if isinstance(event.source, UserSource):
        return await user_service.get_user_by_positions(Position.RND, None)
    return await user_service.get_user_by_positions(Position.RND, event.source.group_id)

async def get_active_dba(event : MessageEvent):
    if isinstance(event.source, UserSource):
        return await user_service.get_user_by_positions(Position.DBA, None)
    return await user_service.get_user_by_positions(Position.DBA, event.source.group_id)

async def get_active_na(event : MessageEvent):
    if isinstance(event.source, UserSource):
        return await user_service.get_user_by_positions(Position.KMG_NA, None)
    return await user_service.get_user_by_positions(Position.KMG_NA, event.source.group_id)

async def get_active_op(event : MessageEvent):
    if isinstance(event.source, UserSource):
        return await user_service.get_user_by_positions(Position.OP, None)
    return await user_service.get_user_by_positions(Position.OP, event.source.group_id)

async def get_active_part(event : MessageEvent):
    if isinstance(event.source, UserSource):
        return await user_service.get_user_by_positions(Position.PART, None)
    return await user_service.get_user_by_positions(Position.PART, event.source.group_id)

async def get_active_resman(event : MessageEvent):
    if isinstance(event.source, UserSource):
        return await user_service.get_user_by_positions(Position.RESMAN, None)
    return await user_service.get_user_by_positions(Position.RESMAN, event.source.group_id)

async def get_active_head(event : MessageEvent):
    if isinstance(event.source, UserSource):
        return await user_service.get_user_by_positions(Position.HEAD, None)
    return await user_service.get_user_by_positions(Position.HEAD, event.source.group_id)

async def sync_line_id(event: MessageEvent):
    args = parse_user_args(event.message.text)
    initial = args[0]
    token = args[1]
    if (token != settings.SYNC_USER_TOKEN):
        return TextMessageV2(text="Invalid sync token.")

    line_id = event.source.user_id
    await user_service.sync_line_id(initial, line_id)
    return TextMessageV2(text=f"Synced {initial} to {line_id}")