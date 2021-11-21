from django.contrib import admin
from django.urls import path

from environment import get_env
from sms import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sms/api/v1/webhook', views.read_sms_from_customer),
    path('sms/api/v1/webhook/scheduler', views.read_sms_from_customer),
    path('', views.redirect_view),
]

print(f"DEBUG_STATUS - {get_env().DEBUG_STATUS}")