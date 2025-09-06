from core import settings
from models.resman import (
    AssistantSemesterData,
    AssistantShift,
    Semester,
    Schedule
)
from .base_repository import BaseRepository

class ResmanRepository(BaseRepository):
    def __init__(self):
        super().__init__(base_url=settings.RESMAN_URL, verify=False)

    async def get_assistant_semester_data(self, positions: list[str]) -> list[AssistantSemesterData]:
        try:
            raw_data = await self.get(f"/Assistant/AssistantSemesterData/Active?Position={';'.join(positions)}")
            return [AssistantSemesterData(**item) for item in raw_data['data']]
        except Exception as e:
            print(f"Error while fetching assistant semester data: {e}")
            raise e

    async def get_assistant_shift(self, initial: str) -> list[AssistantShift]:
        try:
            raw_data = await self.get(f"/Assistant/Shifts?Initial={initial}")
            return [AssistantShift(**item) for item in raw_data['shifts']]
        except Exception as e:
            print(f"Error while fetching assistant shifts: {e}")
            raise e

    async def get_active_semester(self) -> Semester:
        try:
            raw_data = await self.get("/Semester/Active")
            return Semester.model_validate(raw_data["semester"])
        except Exception as e:
            print(f"Error while fetching active semester: {e}")
            raise e

    async def get_schedule_by_initials(self, initials: str, day: str, mid_code: str, semester_id: str) -> list[Schedule]:
        try:
            raw_data = await self.post("/Assistant/ViewSchedule", {
                "initials": initials, "day": day, "midCode": mid_code, "semesterId": semester_id
            })
            return [Schedule(**item) for item in raw_data['schedules']]
        except Exception as e:
            print(f"Error while fetching schedule by initials: {e}")
            raise e

    async def get_schedule_by_position(self, position: str, day: str, mid_code: str, semester_id: str) -> list[Schedule]:
        try:
            raw_data = await self.post("/Assistant/ViewSchedule", {
                "position": position, "day": day, "midCode": mid_code, "semesterId": semester_id
            })
            return [Schedule(**item) for item in raw_data['schedules']]
        except Exception as e:
            print(f"Error while fetching schedule by position: {e}")
            raise e

    async def get_schedule_by_generation(self, generation: str, day: str, mid_code: str, semester_id: str) -> list[Schedule]:
        try:
            raw_data = await self.post("/Assistant/ViewSchedule", {
                "generation": generation, "day": day, "midCode": mid_code, "semesterId": semester_id
            })
            return [Schedule(**item) for item in raw_data['schedules']]
        except Exception as e:
            print(f"Error while fetching schedule by generation: {e}")
            raise e
