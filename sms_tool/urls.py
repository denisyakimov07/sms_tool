from django.contrib import admin
from django.urls import path

import csv

from sms.models import Customer

urlpatterns = [
    path('admin/', admin.site.urls),
]

#sms_customer.csv








