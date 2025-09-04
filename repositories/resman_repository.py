from core.config import settings
from utils.rest import get, post
from models.resman import (
     AssistantSemesterData,
     AssistantShift,
     Semester,
     Schedule
)

        
async def get_assistant_semester_data(positions: list[str]) -> list[AssistantSemesterData]:
    try:
        raw_data = await get(f"{settings.RESMAN_URL}Assistant/AssistantSemesterData/Active?Position={';'.join(positions)}")
        return [AssistantSemesterData(**item) for item in raw_data['data']]
    except Exception as e:
        print(f"An error occurred while getting the assistant semester data: {e}")
        raise e

async def get_assistant_shift(initial: str) -> list[AssistantShift]:
    try:
        raw_data = await get(f"{settings.RESMAN_URL}Assistant/Shifts?Initial={initial}")
        return [AssistantShift(**item) for item in raw_data['shifts']]
    except Exception as e:
        print(f"An error occurred while getting the assistant shift: {e}")
        raise e

async def get_active_semester() -> Semester:
    try:
        raw_data = await get(f"{settings.RESMAN_URL}Semester/Active")
        return Semester.model_validate(raw_data["semester"])
        
    except Exception as e:
        print(f"An error occurred while getting the active semester: {e}")
        raise e 

async def get_schedule_by_initials(initials: str,day: str, mid_code: str,semester_id: str) -> list[Schedule] :
    try:
        raw_data = await post(f"{settings.RESMAN_URL}Assistant/ViewSchedule", {"initials": initials, "day": day, "midCode": mid_code, "semesterId": semester_id})
        print(raw_data)
        return [Schedule(**item) for item in raw_data['schedules']]

    except Exception as e:
        print(f"An error occurred while getting the schedule: {e}")
        raise e

async def get_schedule_by_position(position: str, day: str, mid_code: str,semester_id: str) -> list[Schedule] :
    try:
        raw_data = await post(f"{settings.RESMAN_URL}Assistant/ViewSchedule", {"position": position, "day": day, "midCode": mid_code, "semesterId": semester_id})
        print(raw_data)
        return [Schedule(**item) for item in raw_data['schedules']]

    except Exception as e:
        print(f"An error occurred while getting the schedule: {e}")
        raise e
    
async def get_schedule_by_generation(generation: str, day: str, mid_code: str,semester_id: str) -> list[Schedule] :
    try:
        raw_data = await post(f"{settings.RESMAN_URL}Assistant/ViewSchedule", {"generation": generation, "day": day, "midCode": mid_code, "semesterId": semester_id})
        print(raw_data)
        return [Schedule(**item) for item in raw_data['schedules']]

    except Exception as e:
        print(f"An error occurred while getting the schedule: {e}")
        raise e
