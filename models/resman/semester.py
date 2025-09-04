from pydantic import BaseModel, Field

class Semester(BaseModel):
    semester_id: str = Field(alias='semesterId')
    description: str
    term: str
    isActive: bool
