from database.db import get_database
from models.user_group import UserGroup
from models.groups import Groups
from services.user_service import get_user_by_line_id
from sqlalchemy.orm import joinedload


async def get_group_by_id(group_id: str):
    with get_database() as db:
        return db.query(Groups).filter(Groups.group_id == group_id).first()
    
async def get_member_by_group_id(group_id: str):
    with get_database() as db:
        return db.query(UserGroup).options(joinedload(UserGroup.user)).filter(UserGroup.group_id == group_id).all()
        
async def sync_group_id(group_id: str, group_name: str):
    with get_database() as db:
        try:
            group = await get_group_by_id(group_id)
            if not group:
                group = Groups(group_id=group_id, group_name=group_name)
                db.add(group)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        
async def sync_user_to_group_id(line_id: str, group_id: str):
    with get_database() as db:
        try:
            user = await get_user_by_line_id(line_id)
            if not user:
                raise ValueError(f"No user found with line_id {line_id}")

            group = await get_group_by_id(group_id)
            if not group:
                raise ValueError(f"No user found with group_id` {group_id}")

            link = (
                db.query(UserGroup)
                .filter(UserGroup.user_line_id == user.line_id,
                        UserGroup.group_id == group.group_id)
                .first()
            )
            if not link:
                link = UserGroup(user=user, group=group)
                db.add(link)

            db.commit()

        except Exception as e:
            db.rollback()
            raise e
