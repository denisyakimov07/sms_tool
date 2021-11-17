import datetime

import requests
from requests.auth import  HTTPBasicAuth

from environment import get_env
from sms.models import Customer

API_ENDPOINT = 'https://acuityscheduling.com/api/v1/appointments'


def api_get_appointments(min_date, max_date):
    body = {"minDate": min_date, "maxDate": max_date, "excludeForms": "true", "max": "5000"}
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