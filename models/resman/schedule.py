from pydantic import BaseModel, Field

class ScheduleDetail(BaseModel):
    id: str
    description: str
    type: str
    room: str

class Schedule(BaseModel):
    initial: str
    leader: str
    shift: str
    schedule_details: list[ScheduleDetail | None] = Field(alias='scheduleDetails')