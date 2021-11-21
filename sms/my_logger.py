import datetime

from django.utils import timezone

from sms.email import send_email
from sms.models import Customer, LogIvents

d_now = timezone.now()  # datetime now + time zone


def unsubscribe_customer_log(cus_info: Customer):
    new_log = LogIvents()
    new_log.customer_info = f"{cus_info.first_name} {cus_info.last_name} - {cus_info.phone_number} - {cus_info.email}"
    new_log.status = "unsubscribe"
    new_log.save()


def send_sms_to_customer_log(cus_info: Customer, message_type: str):
    new_log = LogIvents()
    new_log.customer_info = f"{cus_info.first_name} {cus_info.last_name} - {cus_info.phone_number} - {cus_info.email}"
    new_log.status = "sent_sms"
    new_log.message_type = message_type
    new_log.save()


def daily_report():
    total_sms_list = LogIvents.objects.filter(creat__date=d_now - datetime.timedelta(0), status="send_sms")
    unsubscribe_customers = LogIvents.objects.filter(creat__date=d_now - datetime.timedelta(0), status="unsubscribe")

    message = f"Total sent sms - {len(total_sms_list)} \nTotal unsubscribe customers - {len(unsubscribe_customers)}"
    send_email(message)
