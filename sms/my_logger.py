from prettytable import PrettyTable

import datetime

from django.utils import timezone

from sms.email import send_email
from sms.models import Customer, LogIvents
d_now = timezone.now() #datetime now + time zone

def unsubscribe_customer_log(cus_info: Customer):
    new_log = LogIvents()
    new_log.customer_info = f"{cus_info.first_name} {cus_info.last_name} - {cus_info.phone_number} - {cus_info.email}"
    new_log.status = "unsubscribe"
    new_log.save()

def send_sms_to_customer_log(cus_info: Customer, message_type: str):
    new_log = LogIvents()
    new_log.customer_info = f"{cus_info.first_name} {cus_info.last_name} - {cus_info.phone_number} - {cus_info.email}"
    new_log.status = "send_sms"
    new_log.message_type = message_type
    new_log.save()



def report_last_week():
    total_sms_list = LogIvents.objects.filter(creat__range=[d_now - datetime.timedelta(7), d_now], status= "send_sms")
    x = PrettyTable()
    for i in total_sms_list:
        x.add_row(i.customer_info, i.message_type, i.status)
    send_email(x)

