import datetime
import smtplib
import threading
from email.mime.text import MIMEText

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import loader
from loguru import logger

from django.utils import timezone

from environment import get_env
from sms.email_api import send_email, email
from sms.models import Customer, LogIvents, EmailReport, EmailReportRecipient


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

def thread_email_daily_report(background_task):
    threading.Thread(target=background_task).start()

def email_daily_report():
    report_messages = []
    try:
        email_report_list = EmailReport.objects.all()
        email_report_recipient_list = EmailReportRecipient.objects.first()
        for reports in email_report_list:
            customers_list = Customer.objects.filter(last_appointment_date__date=(timezone.now() - datetime.timedelta(365-reports.days)))
            dateISOFormat = (timezone.now() - datetime.timedelta(365-reports.days)).strftime('%x')
            report_messages.append([f" \n \n {dateISOFormat}",[f" \n {customers.first_name} {customers.last_name} *** {customers.phone_number} *** {customers.email}" for customers in customers_list]])
        email_report_recipient_list = email_report_recipient_list.emails_list.replace(' ', '').split(',')
        print(email_report_recipient_list)
        email((''.join(f"{str(mess[0])} {''.join(text for text in mess[1])}" for mess in report_messages)), email_report_recipient_list)

        logger.info("Creat email daily report")
    except Exception as e:
        logger.error("ERROR: Can't creat email daily_report")
        logger.trace(e)

@receiver(post_save, sender=EmailReport)
def post_save_email_report(sender, **kwargs):
    thread_email_daily_report(email_daily_report)


# def email_test():
#     report_messages = {}
#     email_report_list = EmailReport.objects.all()
#     email_report_recipient_list = EmailReportRecipient.objects.first()
#
#     for reports in email_report_list:
#         customers_list = Customer.objects.filter(
#             last_appointment_date__date=(timezone.now() - datetime.timedelta(365 - reports.days)))
#         dateISOFormat = (timezone.now() - datetime.timedelta(365 - reports.days)).strftime('%x')
#         report_messages = {dateISOFormat: customers_list}
#
#
#         # report_messages.append({f"{dateISOFormat}", [
#         #     f" \n {customers.first_name} {customers.last_name} *** {customers.phone_number} *** {customers.email} *** cancel_by_customer {customers.cancel_by_customer}"
#         #     for customers in customers_list]])
#
#
#
#     context = {'data': report_messages}
#     print(context)
#     teml = loader.get_template('../templates/email_templ.html')
#     message = teml.render(context)
#
#
#
#
#     from_whom = "Daily report Bot"
#     server = smtplib.SMTP('smtp.gmail.com:587')
#     server.ehlo()
#     server.starttls()
#     server.login(get_env().MAIL_USERNAME, get_env().MAIL_PASSWORD)
#
#     my_email = MIMEText(message, "html")
#     my_email["From"] = get_env().MAIL_USERNAME
#     my_email["To"] = "you@other.org"
#     my_email["Subject"] = "Hello!"
#
#     server.sendmail(from_whom, 'denisyakimov@gmail.com', my_email.as_string())
#     server.quit()
