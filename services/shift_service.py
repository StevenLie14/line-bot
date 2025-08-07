from linebot.v3.messaging import TextMessageV2
from services import resman_service
from core.constant import day_map, shift_map

async def get_assistant_shift(initial: str):
    try:
        data = await resman_service.get_assistant_shift(initial)

        messages = []

        for entry in data:
            message = [f"Shift schedule for {entry.initial}:", f"{", ".join([shift.shift for shift in entry.shifts])}"]
            for shift in entry.shifts:
                day = day_map.get(shift.day, "Not Found")
                shift_name = shift_map.get(shift.shift, "Not Found")
                message.append(f"Day {day} : {shift_name}")
            messages.append("\n".join(message))

        return TextMessageV2(
            text= "\n\n".join(messages),
        )

    except KeyError:
        return TextMessageV2(text="Failed to retrieve data from RESMAN.")