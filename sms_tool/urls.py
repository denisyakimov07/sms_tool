from django.contrib import admin
from django.urls import path

from environment import get_env
from sms import views
from sms.twilio import send_sms_to_customer


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sms/api/v1/webhook', views.read_sms_from_customer),
]
print(f"DEBUG_STATUS - {get_env().DEBUG_STATUS}")
# send_sms_to_customer(phone_number="4259023584", sms_body='Test')








