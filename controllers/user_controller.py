from linebot.v3.messaging import (
    TextMessageV2, MentionSubstitutionObject, AllMentionTarget
)
import httpx
from core.config import settings
from core.constant import Role, role_map

async def get_active_rnd():
    return TextMessageV2(
            text="Maklo, {everyone}!",
            substitution={
                "everyone": MentionSubstitutionObject(
                    mentionee=AllMentionTarget(type="all")
                )
            }
        )