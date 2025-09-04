from controllers.user_controller import (
    get_active_rnd, sync_line_id, get_active_dba, get_active_na, get_active_head, get_active_op, get_active_resman, get_active_part
)
from controllers.schedule_contoller import (
    get_assistant_shift, get_schedule_by_initials, get_schedule_by_generation, get_schedule_by_position
)
from controllers.group_controller import (
    sync_user_to_group_id, sync_group_id
)
from controllers.request_controller import (
    get_active_tickets
)

ROUTE_MAPS = {
    "/rnd" : get_active_rnd,
    "/dba" : get_active_dba,
    "/na" : get_active_na,
    "/op" : get_active_op,
    "/resman" : get_active_resman,
    "/head" : get_active_head,
    "/part" : get_active_part,
    "/shift" : get_assistant_shift,
    "/sync_id" : sync_line_id,
    "/sync_group" : sync_group_id,
    "/sync_user_group" : sync_user_to_group_id,
    "/schedule" : get_schedule_by_initials,
    "/schedule_gen" : get_schedule_by_generation,
    "/schedule_pos" : get_schedule_by_position,
    "/tickets" : get_active_tickets
}