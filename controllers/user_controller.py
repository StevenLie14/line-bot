from .base_controller import BaseController
from services.user_service import UserService
from core.constant import Position
from linebot.v3.webhooks import MessageEvent, UserSource
from core.config import settings
from linebot.v3.messaging import TextMessageV2
from utils import Helper


class UserController(BaseController):
    def __init__(self, user_service: UserService):
        super().__init__()
        self.user_service = user_service
        self.line_routes = {
            "/rnd": self.get_active_rnd,
            "/dba": self.get_active_dba,
            "/na": self.get_active_na,
            "/op": self.get_active_op,
            "/resman": self.get_active_resman,
            "/head": self.get_active_head,
            "/part": self.get_active_part,
            "/sync_id": self.sync_line_id,
        }

    async def get_active_rnd(self, event: MessageEvent):
        return await self.user_service.get_user_by_positions(Position.RND, event.source.group_id if not isinstance(event.source, UserSource) else None)

    async def get_active_dba(self, event: MessageEvent):
        return await self.user_service.get_user_by_positions(Position.DBA, event.source.group_id if not isinstance(event.source, UserSource) else None)

    async def get_active_na(self, event: MessageEvent):
        return await self.user_service.get_user_by_positions(Position.KMG_NA, event.source.group_id if not isinstance(event.source, UserSource) else None)

    async def get_active_op(self, event: MessageEvent):
        return await self.user_service.get_user_by_positions(Position.OP, event.source.group_id if not isinstance(event.source, UserSource) else None)

    async def get_active_part(self, event: MessageEvent):
        return await self.user_service.get_user_by_positions(Position.PART, event.source.group_id if not isinstance(event.source, UserSource) else None)

    async def get_active_resman(self, event: MessageEvent):
        return await self.user_service.get_user_by_positions(Position.RESMAN, event.source.group_id if not isinstance(event.source, UserSource) else None)

    async def get_active_head(self, event: MessageEvent):
        return await self.user_service.get_user_by_positions(Position.HEAD, event.source.group_id if not isinstance(event.source, UserSource) else None)

    async def sync_line_id(self, event: MessageEvent):
        args = Helper.parse_user_args(event.message.text)
        initial = args[0]
        token = args[1]
        if token != settings.SYNC_USER_TOKEN:
            return TextMessageV2(text="Invalid sync token.")

        line_id = event.source.user_id
        await self.user_service.sync_line_id(initial, line_id)
        return TextMessageV2(text=f"Synced {initial} to {line_id}")
