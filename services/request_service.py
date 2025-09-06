from models.request.ticket import Ticket
from datetime import datetime
from repositories import request_repository
from services import line_service, user_service
from linebot.v3.messaging import UserMentionTarget, MentionSubstitutionObject, TextMessageV2
from core.constant import Position
from core.config import settings

async def format_ticket_summary(tickets : list[Ticket],group_id: str):
    tickets_by_handler = {}
    unassigned_tickets = []
    substitutions= {}
    mention_counter = 1

    try : 
        from services.group_service import get_member_by_group_id
        all_members = await get_member_by_group_id(group_id) if group_id else []
        user_map = {member.user.initial: member.user for member in all_members}

        for ticket in tickets:

            if ticket.handler:
                handler_id = ticket.handler.id
                if handler_id not in tickets_by_handler:
                    tickets_by_handler[handler_id] = {
                        "handler": ticket.handler,
                        "line_user" : user_map.get(ticket.handler.initial),
                        "tickets": []
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
                        type="user",
                        userId=line_user.line_id
                    )
                )
                mention_counter += 1
            handler_block_parts = [
                f"Assigned to {handler.name} ({handler.initial}" +
                (f" {{{placeholder}}}" if line_user else "") + ")"
            ]
            
            for i, ticket in enumerate(assigned_tickets, start=1):
                ticket_detail = (
                    f"{i}. {ticket.title}  ({ticket.ticket_urgency.urgency_name})\n"
                    f"   - ID: {ticket.id}\n"
                    f"   - Status: {ticket.ticket_state.state_name}"
                )
                handler_block_parts.append(ticket_detail)
            
            final_message_parts.append("\n\n".join(handler_block_parts))

        if unassigned_tickets:
            unassigned_block_parts = ["⚠️ Unassigned Tickets (Action Needed)"]
            
            for i, ticket in enumerate(unassigned_tickets, start=1):
                ticket_detail = (
                    f"{i}. {ticket.title}\n"
                    f"   - ID: `{ticket.id}`\n"
                    f"   - Status: {ticket.ticket_state.state_name}\n"
                    f"   - Description: {ticket.description}"
                )
                unassigned_block_parts.append(ticket_detail)

            final_message_parts.append("\n\n".join(unassigned_block_parts))

        closing_message = "Thank you for your cooperation in resolving these tickets promptly."
        final_message_parts.append(closing_message)

        return TextMessageV2(text="\n\n".join(final_message_parts), substitution=substitutions if substitutions else None)
    except KeyError:
        return TextMessageV2(text="Failed to retrieve data from RESMAN.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return TextMessageV2(text="An error occurred while processing the schedule.")

async def format_new_ticket_notification(ticket: Ticket, group_id: str | None):
    try:
        if ticket.ticket_type.type_name in ("DBA"):
            mention = await user_service.get_user_by_positions(Position.DBA, None if group_id is None else group_id)
        else:
            mention = await user_service.get_user_by_positions(Position.RND, None if group_id is None else group_id)

        header = (
            f"{mention.text}\n"
            f"New Ticket Notification - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            "A new ticket has been created and requires attention."
        )

        ticket_block = (
            f"Title: {ticket.title}\n"
            f"ID: {ticket.id}\n"
            f"Urgency: {ticket.ticket_urgency.urgency_name}\n"
            f"Status: {ticket.ticket_state.state_name}\n"
            f"Description: \n{ticket.description or 'No description provided.'}"
        )

        closing = "Please follow up on this ticket as soon as possible."

        return [TextMessageV2(
            text="\n\n".join([header, ticket_block, closing]),
            substitution=mention.substitution
        )]

    except KeyError:
        return TextMessageV2(text="Failed to retrieve data from RESMAN.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return TextMessageV2(text="An error occurred while processing the new ticket.")
    
async def get_active_tickets(group_id: str):
    try:
        tickets = await request_repository.get_active_request()
        return await format_ticket_summary(tickets, group_id)
    except KeyError:
        return TextMessageV2(text="Failed to retrieve data from RESMAN.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return TextMessageV2(text="An error occurred while processing the schedule.")
    
async def notify_new_ticket(ticket: Ticket):
    try:
        messages = await format_new_ticket_notification(ticket, settings.RNDBA_GROUP_ID)
        line_service.send_message(settings.RNDBA_GROUP_ID, messages)
        return "Success"
    except Exception as e:
        print(f"An error occurred: {e}")
        return
    