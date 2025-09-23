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
            "/sync_id": {
                "handler": self.sync_line_id,
                "description": "Sync your Line ID and Initial with the system. Usage: /sync_id <initial> <token>",
                "active": True
            },
            "/rnd": {
                "handler": self.get_active_rnd,
                "description": "Show all active RnD tickets. Usage: /rnd",
                "active": True
            },
            "/dba": {
                "handler": self.get_active_dba,
                "description": "Show all active DBA tickets. Usage: /dba",
                "active": True
            },
            "/na": {
                "handler": self.get_active_na,
                "description": "Show all active NA tickets. Usage: /na",
                "active": True
            },
            "/op": {
                "handler": self.get_active_op,
                "description": "Show all active OP tickets. Usage: /op",
                "active": True
            },
            "/resman": {
                "handler": self.get_active_resman,
                "description": "Show all active Resman tickets. Usage: /resman",
                "active": True
            },
            "/head": {
                "handler": self.get_active_head,
                "description": "Show all active Head tickets. Usage: /head",
                "active": False

            },
            "/part": {
                "handler": self.get_active_part,
                "description": "Show all active Part tickets. Usage: /part",
                "active": False

            }
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
        try:
            initial = args[0]
            token = args[1]
        except IndexError:
            return TextMessageV2(text="Please provide your initial and Token")
        if token != settings.SYNC_USER_TOKEN:
            return TextMessageV2(text="Invalid sync token.")

        line_id = event.source.user_id
        await self.user_service.sync_line_id(initial, line_id)
        return TextMessageV2(text=f"Synced {initial} to {line_id}")

    async def help(self, event: MessageEvent):
        commands = list(self.line_routes.keys())
        commands.sort()
        help_text = "Available commands:\n" + "\n".join(commands)
        return TextMessageV2(text=help_text)
