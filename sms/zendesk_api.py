from loguru import logger

import zenpy
from zenpy import Zenpy
from zenpy.lib.api_objects import Ticket, User, TicketAudit, Comment

from sms.models import Customer, ZenTicket

use_api_token = "kHQsdGfXWHfKVZb0SXk6xRS308bmmA0OX1Kglgqj"
CREDS = {
    'email': 'adam@drnatmed.com',
    'token': use_api_token,
    'subdomain': 'drnatmedco'}

ZENPY_CLIENT = Zenpy(**CREDS)


def zen_create_new_ticket(customer, sms_message: str):
    new_t: TicketAudit() = ZENPY_CLIENT.tickets.create(Ticket(subject="Important",
                              description=sms_message,
                              requester=User(name=f"{customer.first_name} {customer.last_name} {customer.phone_number}",
                              phone=customer.phone_number)))

    return {"ticket_id":new_t.ticket.id, "requester_id" :new_t.ticket.requester_id}


def zen_get_ticket_by_id(id: int):
    try:
        s_ticket: zenpy.lib.api_objects.Ticket = ZENPY_CLIENT.tickets(id=id)
        ticket = s_ticket
    except:
        return None
    if ticket.status == "solved":
        return None
    else:
        ticket.status = "open"
        return ticket


def zen_add_new_message(ticket: zenpy.lib.api_objects.Ticket, message: str, customer, author_id):
    ticket.comment = Comment(body=message, public=True, author_id=author_id)
    ticket.status = "open"
    ticket.recipient = User(name=f"{customer.first_name} {customer.last_name} {customer.phone_number}")
    ZENPY_CLIENT.tickets.update(ticket)


def sms_processor(new_customer: Customer(), sms_text: str):
    zen_ticket = ZenTicket.objects.filter(ticket_status=True, customer=new_customer)
    if zen_ticket:
        zen_ticket = zen_ticket[0]
        zen_ticket_api = zen_get_ticket_by_id(zen_ticket.ticket_id)
        if zen_ticket_api:
            zen_add_new_message(ticket=zen_ticket_api,
                                message=sms_text,
                                customer=new_customer,
                                author_id= zen_ticket.zen_user_id)
        else:
            zen_ticket.ticket_status = False
            zen_ticket.save()
            new_zen_ticket_id = zen_create_new_ticket(new_customer, sms_text)
            new_zen_ticket = ZenTicket()
            new_zen_ticket.ticket_id = new_zen_ticket_id.get("ticket_id")
            new_zen_ticket.customer = new_customer
            new_zen_ticket.ticket_status = True
            new_zen_ticket.zen_user_id = new_zen_ticket_id.get("requester_id")
            new_zen_ticket.save()
            logger.success(f"Create new ticket zen_id={zen_ticket.ticket_id}, phone={zen_ticket.customer.phone_number}")
    else:
        zen_ticket_id = zen_create_new_ticket(new_customer, sms_text)
        zen_ticket = ZenTicket()
        zen_ticket.ticket_id = zen_ticket_id.get("ticket_id")
        zen_ticket.customer = new_customer
        zen_ticket.ticket_status = True
        zen_ticket.zen_user_id = zen_ticket_id.get("requester_id")
        zen_ticket.save()
        logger.success(f"Create new ticket zen_id={zen_ticket.ticket_id}, phone={zen_ticket.customer.phone_number}")


    try:
        pass
    except Exception as e:
        logger.error(f"ERROR: Can't creat ticket")
        logger.trace(e)

