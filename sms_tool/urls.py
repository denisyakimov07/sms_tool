from django.contrib import admin
from django.urls import path

import csv

from sms.models import Customer
from sms.views import update_appointments_for_two_last_days

urlpatterns = [
    path('admin/', admin.site.urls),
]

# update_appointments_for_two_last_days()








