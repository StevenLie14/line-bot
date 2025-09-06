from typing import Dict, Callable

class BaseController:
    def __init__(self):
        self.line_routes: Dict[str, Callable] = {}

    def get_routes(self) -> Dict[str, Callable]:
        return self.line_routes
    

