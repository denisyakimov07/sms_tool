import datetime

from loguru import logger

from django.utils import timezone

from sms.email_api import send_email
from sms.models import Customer, LogIvents




def unsubscribe_customer_log(cus_info: Customer):
    try:
        new_log = LogIvents()
        new_log.customer_info = f"{cus_info.first_name} {cus_info.last_name} - {cus_info.phone_number} - {cus_info.email}"
        new_log.status = "unsubscribe"
        new_log.save()
        logger.info("Unsubscribe log added")
    except Exception as e:
        logger.error("ERROR: Can't add unsubscribe_customer_log")
        logger.trace(e)

def send_sms_to_customer_log(cus_info: Customer, message_type: str):
    try:
        new_log = LogIvents()
        new_log.customer_info = f"{cus_info.first_name} {cus_info.last_name} - {cus_info.phone_number} - {cus_info.email}"
        new_log.status = "sent_sms"
        new_log.message_type = message_type
        new_log.save()
        logger.info("Unsubscribe send_sms_log added")
    except Exception as e:
        logger.error("ERROR: Can't add send_sms_to_customer_log")
        logger.trace(e)

def daily_report():
    try:
        total_sms_list = LogIvents.objects.filter(creat__date=timezone.now(), status="sent_sms")
        unsubscribe_customers = LogIvents.objects.filter(creat__date=timezone.now() - datetime.timedelta(1), status="Incoming sms")
        message = f"Total sent sms - {len(total_sms_list)} \nTotal unsubscribe yesterday customers - {len(unsubscribe_customers)}"
        send_email(message)
        logger.info("Creat daily report")
    except Exception as e:
        logger.error("ERROR: Can't creat daily_report")
        logger.trace(e)