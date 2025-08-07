from linebot.v3.messaging import (
    TextMessageV2, MentionSubstitutionObject, AllMentionTarget
)

def get_active_rnd():
    return TextMessageV2(
            text="Maklo, {everyone}!",
            substitution={
                "everyone": MentionSubstitutionObject(
                    mentionee=AllMentionTarget(type="all")
                )
            }
        )