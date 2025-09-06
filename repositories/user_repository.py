from database.db import get_database
from models import Users

class UserRepository:
    def get_by_line_id(self, line_id: str) -> Users | None:
        with get_database() as db:
            return db.query(Users).filter(Users.line_id == line_id).first()

    def get_all(self) -> list[Users]:
        with get_database() as db:
            return db.query(Users).all()

    def sync_line_id(self, initial: str, line_id: str):
        with get_database() as db:
            try:
                user = db.query(Users).filter(Users.initial == initial.upper()).first()
                if user:
                    user.line_id = line_id
                else:
                    user = Users(initial=initial.upper(), line_id=line_id)
                    db.add(user)
                db.commit()
            except Exception as e:
                db.rollback()
                raise e
