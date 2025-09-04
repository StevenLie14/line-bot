from pydantic import BaseModel,Field

class TicketUrgency(BaseModel):
    id: str
    urgency_name: str = Field(alias="urgencyName")
    urgency_weight: int = Field(alias="urgencyWeight")
    
    