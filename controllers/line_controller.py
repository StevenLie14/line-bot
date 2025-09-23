from fastapi import APIRouter, Request, Header
from services import LineService
from . import BaseController
from linebot.v3.webhooks import MessageEvent

class LineController(BaseController):
    def __init__(self, line_service: LineService):
        super().__init__()
        self.router = APIRouter()
        self.line_service = line_service
        self.line_routes = {
            "/help" : {
                "handler" : self.get_active_routes_message,
                "description" : "Show all available commands. Usage: /help",
                "active" : True
            }
        }
        self._register_routes()

    def _register_routes(self):
        self.router.post("/callback")(self.callback)

    async def callback(self, request: Request, x_line_signature: str = Header(None)):
        body = await request.body()
        return await self.line_service.callback(body, x_line_signature)
    
    def get_active_routes_message(self, event: MessageEvent):
        return self.line_service.get_active_routes_message()
