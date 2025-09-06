from . import BaseController
from services.group_service import GroupService
from linebot.v3.webhooks import MessageEvent
from core import settings
from linebot.v3.messaging import TextMessageV2
from utils import Helper


class GroupController(BaseController):
    def __init__(self, group_service: GroupService):
        super().__init__()
        self.group_service = group_service
        self.line_routes = {
            "/sync_group": self.sync_group_id,
            "/sync_user_group": self.sync_user_to_group_id,
        }

    async def sync_group_id(self, event: MessageEvent):
        args = Helper.parse_user_args(event.message.text)
        group_name = args[0]
        token = args[1]
        if token != settings.SYNC_GROUP_TOKEN:
            return TextMessageV2(text="Invalid sync token.")

        group_id = event.source.group_id
        await self.group_service.sync_group_id(group_id, group_name)
        return TextMessageV2(text=f"Synced {group_id} to {group_name}")

    async def sync_user_to_group_id(self, event: MessageEvent):
        args = Helper.parse_user_args(event.message.text)
        token = args[0]
        if token != settings.SYNC_GROUP_TOKEN:
            return TextMessageV2(text="Invalid sync token.")

        line_id = event.source.user_id
        group_id = event.source.group_id
        await self.group_service.sync_user_to_group_id(line_id, group_id)
        return TextMessageV2(text=f"Synced {line_id} to {group_id}")
