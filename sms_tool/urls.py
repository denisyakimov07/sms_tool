from django.contrib import admin
from django.urls import path

from environment import get_env
from sms import views
from sms.twilio import send_sms_to_customer
from sms.views import get_customers_warning_sms_date_today, get_customers_first_sms_date, get_customers_second_sms_date, \
    get_customers_third_sms_date, get_customers_one_year_sms_date, get_customers_final_warning_7_days_sms_date

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sms/api/v1/webhook', views.read_sms_from_customer),
    path('', views.redirect_view),
]

# send_sms_to_customer(phone_number="4259023584", sms_body='Test')

# get_customers_warning_sms_date_today()
# get_customers_first_sms_date()
# get_customers_second_sms_date()
# get_customers_third_sms_date()
# get_customers_one_year_sms_date()
# get_customers_final_warning_7_days_sms_date()





