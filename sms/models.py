from django.db import models

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=200, null=False, blank=True)
    last_name = models.CharField(max_length=200, null=False, blank=True)
    email = models.CharField(max_length=200, null=False, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    last_appointment_id = models.BigIntegerField(null=False, blank=True)
    last_appointment_date = models.DateTimeField(null=False, blank=True)
    warning_sms_date = models.DateTimeField(null=False, blank=True, default=datetime.now())
    first_sms_date = models.DateTimeField(null=False, blank=True, default=datetime.now())
    second_sms_date = models.DateTimeField(null=False, blank=True, default=datetime.now())
    seven_days_sms = models.DateTimeField(null=False, blank=True, default=datetime.now())
    zero_days_sms = models.DateTimeField(null=False, blank=True, default=datetime.now())
    final_warning_7_days_sms = models.DateTimeField(null=False, blank=True, default=datetime.now())
    cancel_by_customer =  models.BooleanField(blank=True, default=False)


class MainSetup(models.Model):
    warning_sms = models.TextField(null=False, blank=True) # last_appointment_date -30 days
    first_sms_text = models.TextField(null=False, blank=True) #last_appointment_date -21 days
    second_sms_text = models.TextField(null=False, blank=True) #last_appointment_date -14 days
    seven_days = models.TextField(null=False, blank=True)  # last_appointment_date - 7 days
    zero_days= models.TextField(null=False, blank=True) # last_appointment_date = last_appointment_date
    final_warning_7_days_after= models.TextField(null=False, blank=True)  # last_appointment_date +1 year + 7 days
    update_all_users = models.BooleanField(blank=True, default=False)

#API_MODELS

class CustomerAPI(BaseModel):
    appointment_id: Optional[int] = Field(alias='id')
    first_name: Optional[str] = Field(alias='firstName')
    last_name: Optional[str] = Field(alias='lastName')
    phone: Optional[int] = Field(alias='phone')
    email: Optional[str] = Field(alias='email')
    appointment_datetime: Optional[datetime] = Field(alias='datetime')