import django
from django.db import models
from django.utils import timezone

from pydantic import BaseModel, Field
from datetime import datetime


# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=200, null=False, blank=True)
    last_name = models.CharField(max_length=200, null=False, blank=True)
    email = models.CharField(max_length=200, null=False, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True, unique=True)
    last_appointment_id = models.CharField(max_length=500, null=False, blank=True)
    last_appointment_date = models.DateTimeField(null=False, blank=True)
    warning_sms_date = models.DateTimeField(null=True, blank=True)
    second_sms_date = models.DateTimeField(null=True, blank=True)
    third_sms_date = models.DateTimeField(null=True, blank=True)
    one_year_sms_date = models.DateTimeField(null=True, blank=True)
    cancel_by_customer =  models.BooleanField(blank=True, default=False)

    def __str__(self):
        return f"{self.first_name} - {self.last_name} - {self.email}- {self.phone_number} - {self.last_appointment_date}" \
               f"- {self.warning_sms_date} - {self.second_sms_date} - {self.third_sms_date}" \
               f"- {self.one_year_sms_date}"


class MainSetup(models.Model):
    warning_sms = models.TextField(null=False, blank=True) # last_appointment_date -30 days
    second_sms_date = models.TextField(null=False, blank=True) #last_appointment_date -14 days
    third_sms_date = models.TextField(null=False, blank=True)  # last_appointment_date - 7 days
    one_year_sms_date= models.TextField(null=False, blank=True) # last_appointment_date = last_appointment_date
    phone_number = models.CharField(max_length=200, null=False, blank=True)


class CustomerAPIDATA(BaseModel):
    appointment_datetime: datetime = Field(alias='datetime')

class LogIvents(models.Model):
    creat = models.DateTimeField(null=True, blank=True, default=django.utils.timezone.now)
    status = models.TextField(null=True, blank=True)
    customer_info = models.TextField(null=True, blank=True)
    message_type = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.creat} - {self.status} - {self.customer_info}"

class ReportRecipient(models.Model):
    creat = models.DateTimeField(null=True, blank=True, default=django.utils.timezone.now)
    email = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return f"{self.email}"


class FeedbackSMSTemplate(models.Model):
    first_Feedback_sms = models.TextField(null=True, blank=True)
    second_Feedback_sms = models.TextField(null=True, blank=True)
    sent_sms = models.BooleanField(blank=True, default=False)


    def __str__(self):
        return f"{self.first_Feedback_sms} - {self.second_Feedback_sms} - {self.sent_sms}"


class ZenTicket(models.Model):
    ticket_id = models.IntegerField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ticket_status = models.BooleanField(blank=True, default=False)
    zen_user_id = models.BigIntegerField(null=True, blank=True)
    creat = models.DateTimeField(null=True, blank=True, default=django.utils.timezone.now)

    def __str__(self):
        return f"{self.ticket_id} - {self.customer.phone_number} - {self.ticket_status}"
