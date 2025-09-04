from pydantic import BaseModel,Field

class TicketState(BaseModel):
    id: str
    state_name: str = Field(alias="stateName")
    state_description: str = Field(alias="stateDescription")
    
    