from services import shift_service

async def get_assistant_shift(initial: str):
    return await shift_service.get_assistant_shift(initial)