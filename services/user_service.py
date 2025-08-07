from core.constant import Position, position_map
from services.resman_service import get_assistant_semester_data
from linebot.v3.messaging import TextMessageV2, MentionSubstitutionObject, AllMentionTarget
from models.users import Users
from sqlalchemy.orm import Session
import uuid

async def get_user_by_positions(position : Position):
    positions = position_map.get(position,[])
    try:
        response = await get_assistant_semester_data(positions)
        print(response)
        return TextMessageV2(
            text="Maklo, {everyone}!",
            substitution={
                "everyone": MentionSubstitutionObject(
                    mentionee=AllMentionTarget(type="all")
                )
            }
        )
    except KeyError:
        return TextMessageV2(text="Failed to retrieve data from RESMAN.")
    
async def get_user_line_id(initial: str):
    pass

async def sync_line_id(initial: str, line_id: str, db : Session):
    user = Users(id = str(uuid.uuid4()), initial=initial, line_id=line_id)
    db.add(user)
