import datetime

from loguru import logger

from django.utils import timezone

from sms.email_api import send_email, email
from sms.models import Customer, LogIvents, EmailReport


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

def email_daily_report():
    report_messages = []
    try:
        email_report_list = EmailReport.objects.all()
        for reports in email_report_list:
            customers_list = Customer.objects.filter(last_appointment_date__date=(timezone.now() - datetime.timedelta(365-reports.days)))
            dateISOFormat = (timezone.now() - datetime.timedelta(365-reports.days)).strftime('%x')
            report_messages.append([f" \n \n {dateISOFormat}",[f" \n {customers.first_name} - {customers.last_name}- {customers.phone_number} - {customers.email} - cancel_by_customer {customers.cancel_by_customer}" for customers in customers_list]])
        email((''.join(f"{str(mess[0])} {''.join(text for text in mess[1])}" for mess in report_messages)), "DenisYakimov@gmail.com")
        logger.info("Creat email daily report")
    except Exception as e:
        logger.error("ERROR: Can't creat email daily_report")
        logger.trace(e)