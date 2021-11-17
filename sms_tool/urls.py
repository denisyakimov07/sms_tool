from django.contrib import admin
from django.urls import path


from sms.twilio import send_sms_to_customer


urlpatterns = [
    path('admin/', admin.site.urls),
]

# send_sms_to_customer(phone_number="4259023584", sms_body='Test')








