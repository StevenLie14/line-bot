from linebot.v3.messaging import TextMessageV2
from services import resman_service
from core.constant import DAY_MAPS, SHIFT_MAPS, SHIFT_HOURS, SCHEDULE_START_HOUR
from models.resman import Schedule, Semester

async def get_assistant_shift(initial: str):
    try:
        data = await resman_service.get_assistant_shift(initial)

        messages = []

        for entry in data:
            message = [f"Shift schedule for {entry.initial}:", f"{", ".join([shift.shift for shift in entry.shifts])}"]
            for shift in entry.shifts:
                day = DAY_MAPS.get(shift.day, "Not Found")
                shift_name = SHIFT_MAPS.get(shift.shift, "Not Found")
                message.append(f"Day {day} : {shift_name}")
            messages.append("\n".join(message))

        return TextMessageV2(
            text= "\n\n".join(messages),
        )

    except KeyError:
        return TextMessageV2(text="Failed to retrieve data from RESMAN.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return TextMessageV2(text="An error occurred while processing the shift.")
    
def format_schedule(schedules: list[Schedule], semester: Semester) -> TextMessageV2:
    messages = []

    for schedule in schedules:
        schedule_text_parts = []
        
        shift_info = SHIFT_HOURS.get(schedule.shift, {"start": 0, "end": 0, "label": "Unknown"})
        work_start_hour = shift_info["start"]
        work_end_hour = shift_info["end"]

        header = (
            f"Schedule for {schedule.initial}\n\n"
            f"Semester : {semester.description}\n"
            f"Leader: {schedule.leader}\n"
            f"Shift: {schedule.shift} (Work Hours: {shift_info['label']})\n"
            "---"
        )
        schedule_text_parts.append(header)
        
        for i in range(6):
            shift_num = i + 1
            block_start_hour = SCHEDULE_START_HOUR + (i * 2)
            block_end_hour = block_start_hour + 2
            
            block_title = f"Shift {shift_num} ({block_start_hour:02}:00 - {block_end_hour:02}:00) :"

            current_hour = block_start_hour
            detail_index = current_hour - SCHEDULE_START_HOUR
            
            slot_detail = None
            if 0 <= detail_index < len(schedule.scheduleDetails):
                slot_detail = schedule.scheduleDetails[detail_index]
            
            if slot_detail:
                block_title = f"{block_title} {slot_detail.description} ({slot_detail.type})"
            else:
                if work_start_hour <= current_hour < work_end_hour:
                    block_title = f"{block_title} Free"
                else:
                    block_title = f"{block_title} Out of Shift"
            schedule_text_parts.append(block_title)

        messages.append("\n".join(schedule_text_parts))

    return TextMessageV2(
        text="\n\n---\n\n".join(messages),
    )


async def get_schedule_by_generation(generation: str, day: str, mid_code: str):
    try:
        semester = await resman_service.get_active_semester()
        schedules = await resman_service.get_schedule_by_generation(generation, day, mid_code)
        return format_schedule(schedules, semester)

    except KeyError:
        return TextMessageV2(text="Failed to retrieve data from RESMAN.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return TextMessageV2(text="An error occurred while processing the schedule.")

async def get_schedule_by_position(position: str, day: str, mid_code: str):
    try:        
        semester = await resman_service.get_active_semester()
        schedules = await resman_service.get_schedule_by_position(position, day, mid_code)
        return format_schedule(schedules, semester)

    except KeyError:
        return TextMessageV2(text="Failed to retrieve data from RESMAN.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return TextMessageV2(text="An error occurred while processing the schedule.")
    

async def get_schedule_by_initials(initials: str,day: str, mid_code: str):
    try:
        semester = await resman_service.get_active_semester()
        schedules = await resman_service.get_schedule_by_initials(initials, day, mid_code,semester.semesterId)
        return format_schedule(schedules, semester)

    except KeyError:
        return TextMessageV2(text="Failed to retrieve data from RESMAN.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return TextMessageV2(text="An error occurred while processing the schedule.")