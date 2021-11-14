import logging


import requests
from requests.auth import  HTTPBasicAuth

db_logging = logging.getLogger('db')


from environment import get_env
from sms.models import CustomerAPI


API_ENDPOINT = 'https://acuityscheduling.com/api/v1/appointments'

db_logging = logging.getLogger('db')

def api_get_appointments(min_date=None, max_date=None) -> list[CustomerAPI]:
    try:
        body = {"minDate": min_date, "maxDate": max_date, "excludeForms": False}
        response = requests.get(API_ENDPOINT, params=body, auth=HTTPBasicAuth(get_env().ACU_USER_ID, get_env().ACU_API_KEY))
        cus_list = [CustomerAPI(**i) for i in response.json()]

        db_logging.info(f"Get customers from API, total - {len(cus_list)}")
        return cus_list
    except Exception as e:
        db_logging.error(e)










