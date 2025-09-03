from pydantic import BaseModel

class Semester(BaseModel):
    semesterId: str
    description: str
    term: str
    isActive: bool
