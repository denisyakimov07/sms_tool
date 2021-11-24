from twilio.rest import Client
from loguru import logger

# Your Account SID from twilio.com/console
from environment import get_env
from sms.models import Customer
from sms.my_logger import send_sms_to_customer_log


def send_sms_to_customer(customers_list: list[Customer], sms_body: str, message_type=None):
    for customer in customers_list:
        try:
            sms_tex = f"{sms_body.replace('{firstName}', customer.first_name).replace('{lastName}', customer.last_name)}"
            sms_sender(customer.phone_number, sms_tex)
            send_sms_to_customer_log(cus_info=customer, message_type=message_type)
            logger.success(
                f"Sent sms to customer {customer.phone_number}"
                f" - {sms_body.replace('{firstName}', customer.first_name).replace('{lastName}', customer.last_name)}")

        except Exception as e:
            logger.error("ERROR: Can't send_sms_to_customer")
            logger.trace(e)
            send_sms_to_customer_log(cus_info=customer, message_type=str(e))


def sms_sender(phone_number, sms_body):
    try:
        account_sid = get_env().TWILIO_ACCOUNT_SID
        auth_token = get_env().TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to=f"{phone_number}",
            from_="+18449780057",
            body=f"{sms_body}")
        logger.info(f"Message sid - {message.sid}")
    except Exception as e:
        logger.error("ERROR: Can't send sms ")
        logger.trace(e)