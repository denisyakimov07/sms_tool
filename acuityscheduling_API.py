


import requests
from requests.auth import  HTTPBasicAuth




from environment import get_env
from sms.models import CustomerAPI


API_ENDPOINT = 'https://acuityscheduling.com/api/v1/appointments'




def api_get_appointments(min_date=None, max_date=None) -> list[CustomerAPI]:
    body = {"minDate": min_date, "maxDate": max_date, "excludeForms": False}
    response = requests.get(API_ENDPOINT, params=body, auth=HTTPBasicAuth(get_env().ACU_USER_ID, get_env().ACU_API_KEY))
    return [CustomerAPI(**i) for i in response.json()]








