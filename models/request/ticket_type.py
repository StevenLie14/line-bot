from pydantic import BaseModel,Field

class TicketType(BaseModel):
    id: str
    type_name: str = Field(alias="typeName")
    
    