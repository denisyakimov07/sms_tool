from twilio.rest import Client

# Your Account SID from twilio.com/console
from environment import get_env
from sms.models import Customer
from sms.my_logger import send_sms_to_customer_log


def send_sms_to_customer2(customers_list: list[Customer], sms_body: str, message_type=None):
    for customer in customers_list:
        try:
            print(f"{customer.phone_number} - {sms_body.replace('{firstName}', customer.first_name).replace('{lastName}', customer.last_name)}")
            send_sms_to_customer_log(cus_info=customer, message_type=message_type)
        except Exception as e:
            send_sms_to_customer_log(cus_info=customer, message_type=str(e))



def send_sms_to_customer(phone_number, sms_body):
    account_sid = get_env().TWILIO_ACCOUNT_SID
    # Your Auth Token from twilio.com/console
    auth_token  = get_env().TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=f"{phone_number}",
        from_="+17193012173",
        body=f"{sms_body}")
    print(message.sid)