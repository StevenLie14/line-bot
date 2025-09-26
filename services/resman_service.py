from linebot.v3.messaging import TextMessageV2
from repositories import ResmanRepository
from core.constant import DAY_MAPS, SHIFT_MAPS, SHIFT_HOURS, SCHEDULE_START_HOUR, SCHEDULE_END_HOUR
from models.resman import Schedule, Semester


class ResmanService:
    def __init__(self,resman_repository: ResmanRepository):
        self.resman_repository = resman_repository

    async def get_assistant_shift(self, initial: str) -> TextMessageV2:
        try:
            data = await self.resman_repository.get_assistant_shift(initial)

            messages = []

            for entry in data:
                message = [
                    f"Shift schedule for {entry.initial}:",
                    f"{', '.join([shift.shift for shift in entry.shifts])}",
                ]
                for shift in entry.shifts:
                    day = DAY_MAPS.get(shift.day, "Not Found")
                    shift_name = SHIFT_MAPS.get(shift.shift, "Not Found")
                    message.append(f"Day {day} : {shift_name}")
                messages.append("\n".join(message))

            return TextMessageV2(text="\n\n".join(messages))

        except KeyError:
            return TextMessageV2(text="Failed to retrieve data from RESMAN.")
        except Exception as e:
            print(f"An error occurred: {e}")
            return TextMessageV2(
                text="An error occurred while processing the shift."
            )

    def _format_schedule(
        self, schedules: list[Schedule], semester: Semester
    ) -> TextMessageV2:
        messages = []

        for schedule in schedules:
            shift_info = SHIFT_HOURS.get(
                schedule.shift, {"start": 0, "end": 0, "label": "Unknown"}
            )
            work_start_hour = shift_info["start"]
            work_end_hour = shift_info["end"]

            # Header
            header = (
                f"Schedule for {schedule.initial}\n\n"
                f"Semester : {semester.description}\n"
                f"Leader: {schedule.leader}\n"
                f"Shift: {schedule.shift} (Work Hours: {shift_info['label']})\n"
                f"---"
            )

            details = sorted(
                [d for d in schedule.schedule_details if d],
                key=lambda d: d.shift_schedule.start_time,
            )

            body_lines = []
            current_hour = work_start_hour

            for detail in details:
                ss = detail.shift_schedule
                start_h = int(ss.start_time.split(":")[0])
                end_h = int(ss.end_time.split(":")[0])

                if current_hour < start_h:
                    body_lines.append(
                        f"{current_hour:02}:00 - {start_h:02}:00 : Free"
                    )

                body_lines.append(
                    f"{start_h:02}:00 - {end_h:02}:00 : "
                    f"{detail.description} ({detail.type})"
                )

                current_hour = end_h

            if current_hour < work_end_hour:
                body_lines.append(
                    f"{current_hour:02}:00 - {work_end_hour:02}:00 : Free"
                )

            if work_start_hour > SCHEDULE_START_HOUR:
                body_lines.insert(
                    0,
                    f"{SCHEDULE_START_HOUR:02}:00 - {work_start_hour:02}:00 : Out of Shift"
                )
            if work_end_hour < SCHEDULE_END_HOUR:
                body_lines.append(
                    f"{work_end_hour:02}:00 - {SCHEDULE_END_HOUR:02}:00 : Out of Shift"
                )

            messages.append("\n".join([header] + body_lines))

        return TextMessageV2(text="\n\n---\n\n".join(messages))

    async def get_schedule_by_generation(
        self, generation: str, day: str, mid_code: str
    ) -> TextMessageV2:
        try:
            semester = await self.resman_repository.get_active_semester()
            schedules = await self.resman_repository.get_schedule_by_generation(
                generation, day, mid_code
            )
            return self._format_schedule(schedules, semester)

        except KeyError:
            return TextMessageV2(text="Failed to retrieve data from RESMAN.")
        except Exception as e:
            print(f"An error occurred: {e}")
            return TextMessageV2(
                text="An error occurred while processing the schedule."
            )

    async def get_schedule_by_position(
        self, position: str, day: str, mid_code: str
    ) -> TextMessageV2:
        try:
            semester = await self.resman_repository.get_active_semester()
            schedules = await self.resman_repository.get_schedule_by_position(
                position, day, mid_code
            )
            return self._format_schedule(schedules, semester)

        except KeyError:
            return TextMessageV2(text="Failed to retrieve data from RESMAN.")
        except Exception as e:
            print(f"An error occurred: {e}")
            return TextMessageV2(
                text="An error occurred while processing the schedule."
            )

    async def get_schedule_by_initials(
        self, initials: str, day: str, mid_code: str
    ) -> TextMessageV2:
        try:
            semester = await self.resman_repository.get_active_semester()
            schedules = await self.resman_repository.get_schedule_by_initials(
                initials, day, mid_code, semester.semester_id
            )
            return self._format_schedule(schedules, semester)

        except KeyError:
            return TextMessageV2(text="Failed to retrieve data from RESMAN.")
        except Exception as e:
            print(f"An error occurred: {e}")
            return TextMessageV2(
                text="An error occurred while processing the schedule."
            )
