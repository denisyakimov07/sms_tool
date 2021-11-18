from django.contrib import admin
from django.urls import path

from sms import views
from sms.email import send_email
from sms.my_logger import report_last_week
from sms.views import get_customers_warning_sms_date_today, get_customers_first_sms_date, get_customers_second_sms_date, \
    get_customers_third_sms_date, get_customers_one_year_sms_date, get_customers_final_warning_7_days_sms_date

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sms/api/v1/webhook', views.read_sms_from_customer),
    path('', views.redirect_view),
]



# get_customers_warning_sms_date_today()
# get_customers_first_sms_date()
# get_customers_second_sms_date()
# get_customers_third_sms_date()
# get_customers_one_year_sms_date()
# get_customers_final_warning_7_days_sms_date()




# report_last_week()