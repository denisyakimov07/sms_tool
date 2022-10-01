from django.contrib import admin
from django.urls import path

from sms import views
from sms.my_logger import thread_email_daily_report, email_daily_report

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sms/api/v1/webhook', views.read_sms_from_customer),
    path('sms/api/v1/webhook/scheduler', views.scheduler),
    path('sms/api/v1/webhook/zendesk', views.zendesk_webhook),
    path('', views.redirect_view),
]

thread_email_daily_report(email_daily_report)