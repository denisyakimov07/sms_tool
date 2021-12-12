from django.contrib import admin
from django.urls import path

from sms import views
from sms.models import Customer
from sms.views import feedback_sms_sender
from sms.zendesk_api import sms_processor

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sms/api/v1/webhook', views.read_sms_from_customer),
    path('sms/api/v1/webhook/scheduler', views.scheduler),
    path('sms/api/v1/webhook/zendesk', views.zendesk_webhook),
    path('', views.redirect_view),
]

# sms_processor(new_customer = Customer.objects.filter(phone_number__contains=8312168131)[0], sms_text= "Test dsadsaads111")
