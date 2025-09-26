from pydantic import BaseModel, Field
from .shift_schedule import ShiftSchedule

class ScheduleDetail(BaseModel):
    id: str
    description: str
    type: str
    room: str
    shift_schedule : ShiftSchedule = Field(alias='shiftSchedule')

class Schedule(BaseModel):
    initial: str
    leader: str
    shift: str
    schedule_details: list[ScheduleDetail | None] = Field(alias='scheduleDetails')