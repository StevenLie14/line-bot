from typing import Optional
from models import Route

class LineRouteRegistry:
    def __init__(self):
        self.routes = {}
    
    def register_routes(self, routes: dict[str,Route]):
        self.routes.update(routes)
        
    def get_route(self, command: str) -> Optional[Route]:
        return self.routes.get(command)
        
    def get_active_routes(self) -> dict[str, Route]:
        return {cmd: route for cmd, route in self.routes.items() if route["active"]}
    
