from controllers.user_controller import (
    get_active_rnd, sync_line_id, get_active_dba, get_active_na
)
from controllers.shift_contoller import (
    get_assistant_shift
)

route_map = {
    "/rnd" : get_active_rnd,
    "/dba" : get_active_dba,
    "/na" : get_active_na,
    "/shift" : get_assistant_shift,
    "/sync" : sync_line_id,
}