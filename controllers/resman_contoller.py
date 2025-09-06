from services import ResmanService
from linebot.v3.webhooks import MessageEvent
from utils import Helper
from linebot.v3.messaging import TextMessageV2
from . import BaseController

class ResmanController(BaseController):
    def __init__(self, resman_service: ResmanService):
        super().__init__()
        self.resman_service = resman_service
        self.line_routes = {
            "/schedule": self.get_schedule_by_initials,
            "/schedule_gen": self.get_schedule_by_generation ,
            "/schedule_pos": self.get_schedule_by_position,
        }
        
    async def get_assistant_shift(self, event: MessageEvent):
        args = Helper.parse_user_args(event.message.text)
        try:
            initial = args[0]
        except IndexError:
            return TextMessageV2(text="Please provide your initial")
        return await self.resman_service.get_assistant_shift(initial)

    async def get_schedule_by_initials(self, event: MessageEvent):
        args = Helper.parse_user_args(event.message.text)
        try:
            initials = args[0]
            day = args[1]
            mid_code = args[2]
        except IndexError:
            return TextMessageV2(
                text="Please provide your initials, the day, and the mid code."
            )
        return await self.resman_service.get_schedule_by_initials(initials, day, mid_code)

    async def get_schedule_by_position(self, event: MessageEvent):
        args = Helper.parse_user_args(event.message.text)
        try:
            position = args[0]
            day = args[1]
            mid_code = args[2]
        except IndexError:
            return TextMessageV2(
                text="Please provide your position, the day, and the mid code."
            )
        return await self.resman_service.get_schedule_by_position(position, day, mid_code)

    async def get_schedule_by_generation(self, event: MessageEvent):
        args = Helper.parse_user_args(event.message.text)
        try:
            generation = args[0]
            day = args[1]
            mid_code = args[2]
        except IndexError:
            return TextMessageV2(
                text="Please provide your generation, the day, and the mid code."
            )
        return await self.resman_service.get_schedule_by_generation(generation, day, mid_code)
