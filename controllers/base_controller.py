from typing import Dict
from models import Route

class BaseController:
    def __init__(self):
        self.line_routes: Dict[str, Route] = {}

    def get_routes(self) -> Dict[str, Route]:
        return self.line_routes

