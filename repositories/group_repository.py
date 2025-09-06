from database.db import get_database
from models.user_group import UserGroup
from models.groups import Groups
from sqlalchemy.orm import joinedload

class GroupRepository:
    def get_group_by_id(self, group_id: str) -> Groups | None:
        with get_database() as db:
            return db.query(Groups).filter(Groups.group_id == group_id).first()

    def get_members_by_group_id(self, group_id: str) -> list[UserGroup]:
        with get_database() as db:
            return (
                db.query(UserGroup)
                .options(joinedload(UserGroup.user))
                .filter(UserGroup.group_id == group_id)
                .all()
            )

    def sync_group_id(self, group_id: str, group_name: str):
        with get_database() as db:
            try:
                group = self.get_group_by_id(group_id)
                if not group:
                    group = Groups(group_id=group_id, group_name=group_name)
                    db.add(group)
                db.commit()
            except Exception as e:
                db.rollback()
                raise e

    def sync_user_to_group_id(self, user, group):
        with get_database() as db:
            try:
                link = (
                    db.query(UserGroup)
                    .filter(
                        UserGroup.user_line_id == user.line_id,
                        UserGroup.group_id == group.group_id,
                    )
                    .first()
                )
                if not link:
                    link = UserGroup(user=user, group=group)
                    db.add(link)
                db.commit()
            except Exception as e:
                db.rollback()
                raise e
