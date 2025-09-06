from repositories import UserRepository, ResmanRepository, GroupRepository
from linebot.v3.messaging import UserMentionTarget, MentionSubstitutionObject, TextMessageV2
from core.constant import Position, POSITION_MAPS


class UserService:
    def __init__(self, user_repository: UserRepository,
                 resman_repository: ResmanRepository,
                 group_repository: GroupRepository):
        self.user_repository = user_repository
        self.resman_repository = resman_repository
        self.group_repository = group_repository

    async def get_user_by_line_id(self, line_id: str):
        return self.user_repository.get_by_line_id(line_id)

    async def get_all_users(self):
        return self.user_repository.get_all()

    async def sync_line_id(self, initial: str, line_id: str):
        return self.user_repository.sync_line_id(initial, line_id)
    
    async def get_user_by_positions(self, position: Position, group_id: str):
        positions = POSITION_MAPS.get(position, [])
        ast_data = await self.resman_repository.get_assistant_semester_data(positions)

        if group_id is None:
            text_template_parts = [f"@{ast.initial}" for ast in ast_data]
            return TextMessageV2(text="Dear, " + " ".join(text_template_parts) + "!")

        try:
            all_members = self.group_repository.get_members_by_group_id(group_id)
            user_map = {member.user.initial: member.user for member in all_members}
            
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
                            userId=user.line_id,
                        ),
                    )
                else:
                    text_template_parts.append(f"@{initial}")
                mention_count += 1

            final_text = "Dear, " + " ".join(text_template_parts) + "!"
            return TextMessageV2(
                text=final_text,
                substitution=substitution_objects if substitution_objects else None,
            )

        except Exception as e:
            print(f"An error occurred: {e}")
            return TextMessageV2(text="Failed to retrieve data from RESMAN.")

