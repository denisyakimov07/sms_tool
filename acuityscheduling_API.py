import datetime
import json

import requests
from requests.auth import  HTTPBasicAuth
import pprint


from environment import get_env
from sms.models import Customer, CustomerAPIDATA
from sms.views import add_to_db_all_customers

API_ENDPOINT = 'https://acuityscheduling.com/api/v1/appointments'



# def api_get_appointments(min_date=None, max_date=None) -> list[Customer]:
#     try:
#         body = {"minDate": min_date, "maxDate": max_date, "excludeForms": False, "max":"20"}
#         response = requests.get(API_ENDPOINT, params=body, auth=HTTPBasicAuth(get_env().ACU_USER_ID, get_env().ACU_API_KEY))
#         cus_list = [CustomerAPI(**i) for i in response.json()]
#         print(f"Get customers from API, total - {len(cus_list)}")
#         return cus_list
#     except Exception as e:
#         print(e)



def api_get_appointments(min_date, max_date):
    body = {"minDate": min_date, "maxDate": max_date, "excludeForms": "true", "max": "2000"}
    response = requests.get(API_ENDPOINT, params=body, auth=HTTPBasicAuth(get_env().ACU_USER_ID, get_env().ACU_API_KEY))
    cus_list = []
    for res in response.json():
        customer_from_api = Customer()
        customer_from_api.first_name = res.get('firstName')
        customer_from_api.last_name = res.get('lastName')
        customer_from_api.phone_number = res.get('phone')
        customer_from_api.email = res.get('email')

        dt_obj = datetime.datetime.strptime(f"{res.get('datetime')}", '%Y-%m-%dT%H:%M:%S%z')
        customer_from_api.last_appointment_date = dt_obj

        customer_from_api.last_appointment_id = res.get('confirmationPage')
        cus_list.append(customer_from_api)


    return cus_list


def one_time_load_all_customers():
    cus_list =  api_get_appointments(min_date=datetime.datetime.strptime("2021-08-01", "%Y-%m-%d"), max_date=datetime.datetime.strptime("2021-12-01", "%Y-%m-%d"))
    add_to_db_all_customers(cus_list)

from django.utils import timezone
datetime_now = timezone.now()

def get_warning_sms_date_customers():
    s_data = datetime_now + datetime.timedelta(1)

    list = Customer.objects.filter(warning_sms_date__date=s_data)
    print(f"{s_data}  --  {len(list)}")

    # for i in list:
    #     print (i)



