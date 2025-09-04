from pydantic import BaseModel, Field
from datetime import datetime
from models.request.user import User
from models.request.ticket_state import TicketState
from models.request.ticket_urgency import TicketUrgency
from models.request.ticket_type import TicketType

class Ticket(BaseModel):
    id: str
    title: str
    description: str
    solvedAt: datetime
    createdDate: datetime
    creator: User
    handler: User
    ticket_state: TicketState = Field(alias="ticketState")
    ticket_urgency: TicketUrgency = Field(alias="ticketUrgency")
    ticket_type: TicketType = Field(alias="ticketType")

    