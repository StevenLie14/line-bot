from pydantic import BaseModel, Field

class ShiftSchedule(BaseModel):
    shift_schedule_id: str = Field(alias='shiftScheduleId')
    name: str
    start_time : str = Field(alias='startTime')
    end_time : str = Field(alias='endTime')
    created_at: str = Field(alias='createdAt')
    updated_at: str = Field(alias='updatedAt')
    