from services import resman_service
from linebot.v3.webhooks import MessageEvent
from utils.helper import parse_user_args
from linebot.v3.messaging import TextMessageV2
    # line_service.send_message("U07a7890f1a03d16370198ffeb071f201", "test")

async def get_assistant_shift(event : MessageEvent):
    args = parse_user_args(event.message.text)
    try:
        initial = args[0]
    except IndexError:
        return TextMessageV2(text="Please provide your initial")
    return await resman_service.get_assistant_shift(initial)

async def get_schedule_by_initials(event : MessageEvent):
    args = parse_user_args(event.message.text)
    try:
        initials = args[0]
        day = args[1]
        mid_code = args[2]
    except IndexError:
        return TextMessageV2(text="Please provide your initials, the day, and the mid code.")
    return await resman_service.get_schedule_by_initials(initials,day,mid_code)

async def get_schedule_by_position(event: MessageEvent):
    args = parse_user_args(event.message.text)
    try: 
        position = args[0]
        day = args[1]
        mid_code = args[2]
    except IndexError:
        return TextMessageV2(text="Please provide your position, the day, and the mid code.")
    return await resman_service.get_schedule_by_position(position,day,mid_code)

async def get_schedule_by_generation(event: MessageEvent):
    args = parse_user_args(event.message.text)
    try: 
        generation = args[0]
        day = args[1]
        mid_code = args[2]
    except IndexError:
        return TextMessageV2(text="Please provide your generation, the day, and the mid code.")
    return await resman_service.get_schedule_by_generation(generation,day,mid_code)