from django.db import models

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=200, null=False, blank=True)
    last_name = models.CharField(max_length=200, null=False, blank=True)
    email = models.CharField(max_length=200, null=False, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    last_appointment_id = models.BigIntegerField(null=False, blank=True)
    last_appointment_date = models.DateTimeField(null=False, blank=True)
    warning_sms_date = models.DateTimeField(null=False, blank=True)
    first_sms_date = models.DateTimeField(null=False, blank=True)
    second_sms_date = models.DateTimeField(null=False, blank=True)
    cancel_by_customer =  models.BooleanField(blank=True, default=False)
    def __str__(self):
        return self.phone_number

class MainSetup(models.Model):
    warning_sms = models.TextField(null=False, blank=True) # last_appointment_date -30 days
    first_sms_text = models.TextField(null=False, blank=True) #last_appointment_date -21 days
    second_sms_text = models.TextField(null=False, blank=True) #last_appointment_date -14 days
    seven_days = models.TextField(null=False, blank=True)  # last_appointment_date - 7 days
    zero_days= models.TextField(null=False, blank=True) # last_appointment_date = last_appointment_date
    final_warning_7_days_after= models.TextField(null=False, blank=True)  # last_appointment_date +1 year + 7 days
