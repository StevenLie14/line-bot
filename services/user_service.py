from core.constant import Position, position_map
from services.resman_service import get_assistant_semester_data
from linebot.v3.messaging import UserMentionTarget, MentionSubstitutionObject, TextMessageV2
from database.db import get_database
from models.users import Users
import uuid

async def get_user_by_positions(position: Position):
    positions = position_map.get(position, [])
    
    try:
        all_users = await get_all_users()
        user_map = {user.initial: user for user in all_users}
        
        ast_data = await get_assistant_semester_data(positions)

        text_template_parts = []
        substitution_objects = {}
        mention_count = 1

        for ast in ast_data:
            initial = ast.initial
            placeholder = f"user{mention_count}"
            user = user_map.get(initial)

            if user:
                text_template_parts.append(f"{{{placeholder}}}")
                substitution_objects[placeholder] = MentionSubstitutionObject(
                    type="mention",
                    mentionee=UserMentionTarget(
                        type="user",
                        userId=user.line_id
                    )
                )
            else:
                text_template_parts.append(f"@{initial}")

            mention_count += 1

        final_text = "Maklo, " + " ".join(text_template_parts) + "!"

        return TextMessageV2(
            text=final_text,
            substitution=substitution_objects if substitution_objects else None
        )

    except KeyError:
        return TextMessageV2(text="Failed to retrieve data from RESMAN.")
    
async def get_all_users():
    with get_database() as db:
        return db.query(Users).all()
    
async def sync_line_id(initial: str, line_id: str):
    with get_database() as db:
        try:
            user = db.query(Users).filter(Users.initial == initial.upper()).first()
            if user:
                user.line_id = line_id
            else:
                user = Users(id=str(uuid.uuid4()), initial=initial.upper(), line_id=line_id)
                db.add(user)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
