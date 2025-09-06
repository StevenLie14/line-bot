from repositories import GroupRepository


class GroupService:
    def __init__(self, group_repository: GroupRepository):
        self.group_repository = group_repository

    async def get_member_by_group_id(self, group_id: str):
        return self.group_repository.get_members_by_group_id(group_id)
    
    async def sync_group_id(self, group_id: str, group_name: str):
        return self.group_repository.sync_group_id(group_id, group_name)
    
    async def sync_user_to_group_id(self, user, group):
        return self.group_repository.sync_user_to_group_id(user, group)
    

    