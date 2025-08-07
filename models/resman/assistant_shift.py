from pydantic import BaseModel

class AssistantShiftDetail(BaseModel):
    day: int
    shift: str

class AssistantShift(BaseModel):
    initial: str
    shifts: list[AssistantShiftDetail]