from django.contrib import admin
from django.urls import path

from sms import views
from sms.views import feedback_sms_sender

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sms/api/v1/webhook', views.read_sms_from_customer),
    path('sms/api/v1/webhook/scheduler', views.scheduler),
    path('', views.redirect_view),
]

