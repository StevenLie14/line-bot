from typing import Callable, Optional

class LineRouteRegistry:
    def __init__(self):
        self.routes = {}
    
    def register_routes(self, routes: dict[str,callable]):
        self.routes.update(routes)
        
    def get_route(self, command: str) -> Optional[Callable]:
        return self.routes.get(command)
        
    
