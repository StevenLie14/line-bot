from services.user_service import get_user_by_positions
from core.constant import Position

async def get_active_rnd():
    return await get_user_by_positions(Position.RND)