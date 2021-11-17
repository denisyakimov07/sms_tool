from twilio.rest import Client

# Your Account SID from twilio.com/console
from environment import get_env


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