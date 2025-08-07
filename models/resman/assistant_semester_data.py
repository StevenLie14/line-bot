from pydantic import BaseModel

class AssistantSemesterData(BaseModel):
    initial: str
    position: str
    leader: str