from linebot.v3.webhooks import MessageEvent
from core.config import settings
from linebot.v3.messaging import TextMessageV2
from services import group_service
from utils.helper import parse_user_args

async def sync_group_id(event: MessageEvent):
    args = parse_user_args(event.message.text)
    group_name = args[0]
    token = args[1]
    if (token != settings.SYNC_GROUP_TOKEN):
        return TextMessageV2(text="Invalid sync token.")
    
    group_id = event.source.group_id
    await group_service.sync_group_id(group_id, group_name)
    return TextMessageV2(text=f"Synced {group_id} to {group_name}")


async def sync_user_to_group_id(event: MessageEvent):
    args = parse_user_args(event.message.text)
    token = args[0]
    if (token != settings.SYNC_GROUP_TOKEN):
        return TextMessageV2(text="Invalid sync token.")

    line_id = event.source.user_id
    group_id = event.source.group_id
    await group_service.sync_user_to_group_id(line_id, group_id)
    return TextMessageV2(text=f"Synced {line_id} to {group_id}")