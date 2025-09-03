from pydantic import BaseModel

class ScheduleDetail(BaseModel):
    id: str
    description: str
    type: str
    room: str

class Schedule(BaseModel):
    initial: str
    leader: str
    shift: str
    scheduleDetails: list[ScheduleDetail | None] 