from django.contrib import admin

# Register your models here.
from .models import Customer, MainSetup


class MainSetupAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class CustomeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "phone_number", "email", "last_appointment_date",
                    "warning_sms_date", "first_sms_date", "second_sms_date", "seven_days_sms", "zero_days_sms",
                    "final_warning_7_days_sms", "cancel_by_customer", "last_appointment_id")
    def first_name(self, obj):
        return obj.first_name

    def last_name(self, obj):
        return obj.last_name

    def phone_number(self, obj):
        return obj.phone_number

    def email(self, obj):
        return obj.email

    def last_appointment_date(self, obj):
        return obj.last_appointment_date


    def last_appointment_id(self, obj):
        return obj.last_appointment_id

    def warning_sms_date(self, obj):
        return obj.warning_sms_date

    def first_sms_date(self, obj):
        return obj.first_sms_date

    def second_sms_date(self, obj):
        return obj.second_sms_date

    def cancel_by_customer(self, obj):
        return obj.cancel_by_customer

    def zero_days_sms(self, obj):
        return obj.zero_days_sms

    def final_warning_7_days_sms(self, obj):
        return obj.final_warning_7_days_sms




admin.site.register(Customer, CustomeAdmin)
admin.site.register(MainSetup, MainSetupAdmin)

