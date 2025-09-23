from datetime import datetime
from models.request import Ticket
from repositories import RequestRepository, GroupRepository
from services.line_service import LineService
from services.user_service import UserService
from linebot.v3.messaging import (
    UserMentionTarget,
    MentionSubstitutionObject,
    TextMessageV2,
)
from core import Position, settings
from models import UserGroup
from utils import Helper


class RequestService:
    def __init__(self, request_repository: RequestRepository, line_service: LineService,
                 user_service: UserService, group_repository: GroupRepository):
        self.request_repository = request_repository
        self.line_service = line_service
        self.user_service = user_service
        self.group_repository = group_repository

    async def format_ticket_summary(self, tickets: list[Ticket], group_id: str):
        tickets_by_handler = {}
        unassigned_tickets = []
        substitutions = {}
        mention_counter = 1

        try:
            all_members =  self.group_repository.get_members_by_group_id(group_id) if group_id else []
            user_map = {member.user.initial: member.user for member in all_members}

            for ticket in tickets:
                if ticket.handler:
                    handler_id = ticket.handler.id
                    if handler_id not in tickets_by_handler:
                        tickets_by_handler[handler_id] = {
                            "handler": ticket.handler,
                            "line_user": user_map.get(ticket.handler.initial),
                            "tickets": [],
                        }
                    tickets_by_handler[handler_id]["tickets"].append(ticket)
                else:
                    unassigned_tickets.append(ticket)

            final_message_parts = []

            main_header = (
                f"Subject: Daily Recap of All Open Tickets - {datetime.now().strftime('%Y-%m-%d')}\n"
                "This is a summary of all tickets that are still open and require action. "
                "Please follow up on your assigned tickets accordingly."
            )
            final_message_parts.append(main_header)

            for handler_id, data in tickets_by_handler.items():
                handler = data["handler"]
                assigned_tickets = data["tickets"]
                line_user = data["line_user"]
                placeholder = f"user{mention_counter}"

                if line_user:
                    substitutions[placeholder] = MentionSubstitutionObject(
                        type="mention",
                        mentionee=UserMentionTarget(
                            type="user", userId=line_user.line_id
                        ),
                    )
                    mention_counter += 1
                handler_block_parts = [
                    f"Assigned to {handler.name} ({handler.initial}"
                    + (f" {{{placeholder}}}" if line_user else "")
                    + ")"
                ]

                for i, ticket in enumerate(assigned_tickets, start=1):
                    ticket_detail = (
                        f"{i}. {ticket.title}  ({ticket.ticket_urgency.urgency_name})\n"
                        f"   - Status: {ticket.ticket_state.state_name}"
                        f"   - Creator: {ticket.creator.initial} ({ticket.creator.name})"
                    )
                    handler_block_parts.append(ticket_detail)

                final_message_parts.append("\n\n".join(handler_block_parts))

            if unassigned_tickets:
                unassigned_block_parts = ["⚠️ Unassigned Tickets (Action Needed)"]

                for i, ticket in enumerate(unassigned_tickets, start=1):
                    ticket_detail = (
                        f"{i}. {ticket.title}\n"
                        f"   - Status: {ticket.ticket_state.state_name}\n"
                        f"   - Description: {ticket.description}"
                    )
                    unassigned_block_parts.append(ticket_detail)

                final_message_parts.append("\n\n".join(unassigned_block_parts))

            closing_message = "Thank you for your cooperation in resolving these tickets promptly."
            final_message_parts.append(closing_message)

            return TextMessageV2(
                text="\n\n".join(final_message_parts),
                substitution=substitutions if substitutions else None,
            )
        except KeyError:
            return TextMessageV2(text="Failed to retrieve data from RESMAN.")
        except Exception as e:
            print(f"An error occurred: {e}")
            return TextMessageV2(
                text="An error occurred while processing the schedule."
            )

    async def format_new_ticket_notification(
        self, ticket: Ticket, group_id: str | None
    ):
        try:
            if ticket.ticket_type.type_name in ("DBA"):
                mention = await self.user_service.get_user_by_positions(
                    Position.DBA, None if group_id is None else group_id
                )
            else:
                mention = await self.user_service.get_user_by_positions(
                    Position.RND, None if group_id is None else group_id
                )

            message = (
                f"{mention.text}\n"
                f"New Ticket Notification - {Helper.get_current_time()}\n"
                "A new ticket has been created and requires attention.\n\n"
                f"Title: {ticket.title}\n"
                f"Urgency: {ticket.ticket_urgency.urgency_name}\n"
                f"Status: {ticket.ticket_state.state_name}\n"
                f"Creator: {ticket.creator.initial} ({ticket.creator.name})\n"
                f"Description: \n{ticket.description or 'No description provided.'}\n"
                f"Description: \n\n{ticket.description or 'No description provided.'}\n\n"
                "Please follow up on this ticket as soon as possible."
            )

            return TextMessageV2(
                    text=message,
                    substitution=mention.substitution,
                )
            

        except KeyError:
            return TextMessageV2(text="Failed to retrieve data from RESMAN.")
        except Exception as e:
            print(f"An error occurred: {e}")
            return TextMessageV2(
                text="An error occurred while processing the new ticket."
            )

    async def get_active_tickets(self, group_id: str):
        try:
            tickets = await self.request_repository.get_active_request()
            return await self.format_ticket_summary(tickets, group_id)
        except KeyError:
            return TextMessageV2(text="Failed to retrieve data from RESMAN.")
        except Exception as e:
            print(f"An error occurred: {e}")
            return TextMessageV2(
                text="An error occurred while processing the schedule."
            )

    async def notify_new_ticket(self, ticket: Ticket):
        try:
            messages = await self.format_new_ticket_notification(
                ticket, settings.RNDBA_GROUP_ID
            )
            self.line_service.send_message(settings.RNDBA_GROUP_ID, [messages])
            return "Success"
        except Exception as e:
            print(f"An error occurred: {e}")
            return "Failed"
