from django.contrib import admin

# Register your models here.
from .models import Customer, MainSetup, LogIvents, ReportRecipient, FeedbackSMSTemplate, EmailReport, \
    EmailReportRecipient

admin.site.site_header = 'Doctors of Natural Medicine SMS Tool'
admin.site.site_title = 'Doctors of Natural Medicine'
admin.site.index_title = 'Doctors of Natural Medicine'


class MainSetupAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class CustomeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "phone_number", "email", "last_appointment_date",
                    "warning_sms_date", "second_sms_date", "third_sms_date", "one_year_sms_date",
                    "cancel_by_customer", "last_appointment_id")
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

    def warning_sms_date(self, obj):
        return obj.warning_sms_date

    def second_sms_date(self, obj):
        return obj.second_sms_date

    def third_sms_date(self, obj):
        return obj.third_sms_date

    def one_year_sms_date(self, obj):
        return obj.one_year_sms_date


    def cancel_by_customer(self, obj):
        return obj.cancel_by_customer

    def last_appointment_id(self, obj):
        return obj.last_appointment_id

    search_fields = ("phone_number", "email")

class LogIventsAdmin(admin.ModelAdmin):
    list_display = ("customer_info", "message_type", "status", "creat")

    def customer_info(self, obj):
        return obj.customer_info

    def message_type(self, obj):
        return obj.message_type

    def status(self, obj):
        return obj.status

    def creat(self, obj):
        return obj.creat

    search_fields = ("customer_info", "message_type", "status")

class ReportRecipientAdmin(admin.ModelAdmin):
    list_display = ("email", "creat")

    def email(self, obj):
        return obj.email

    def creat(self, obj):
        return obj.creat


class FeedbackSMSTemplateAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class EmailReportRecipientAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Customer, CustomeAdmin)
admin.site.register(MainSetup, MainSetupAdmin)
admin.site.register(LogIvents, LogIventsAdmin)
admin.site.register(ReportRecipient, ReportRecipientAdmin)
admin.site.register(EmailReport)
admin.site.register(EmailReportRecipient, EmailReportRecipientAdmin)
admin.site.register(FeedbackSMSTemplate, FeedbackSMSTemplateAdmin)
