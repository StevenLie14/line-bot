from controllers.user_controller import (
    get_active_rnd, sync_line_id, get_active_dba, get_active_na, get_active_head, get_active_op, get_active_resman, get_active_part
)
from controllers.shift_contoller import (
    get_assistant_shift
)

route_map = {
    "/rnd" : get_active_rnd,
    "/dba" : get_active_dba,
    "/na" : get_active_na,
    "/op" : get_active_op,
    "/resman" : get_active_resman,
    "/head" : get_active_head,
    "/part" : get_active_part,
    "/shift" : get_assistant_shift,
    "/sync" : sync_line_id,
}