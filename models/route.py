from typing import Dict, Callable, TypedDict

class Route(TypedDict):
    handler: Callable
    description: str
    active: bool