from datetime import datetime


import requests

from pydantic import BaseModel, Field
from typing import Optional



from environment import get_env

API_ENDPOINT = 'https://acuityscheduling.com/api/v1/appointments'

class CustomerAPI(BaseModel):
    appointment_id: int = Field(alias='id')
    first_name: Optional[str] = Field(alias='firstName')
    last_name: Optional[str] = Field(alias='lastName')
    phone: Optional[int] = Field(alias='phone')
    email: Optional[str] = Field(alias='email')
    appointment_datetime: Optional[datetime] = Field(alias='datetime')


def api_get_appointments(min_date=None, max_date=None) -> list[CustomerAPI]:
    body = {"minDate":min_date, "maxDate":max_date, "excludeForms":False}
    session = requests.Session()
    session.auth = get_env().USER_ID, get_env().API_KEY
    session.post(API_ENDPOINT)
    response = session.get(API_ENDPOINT, params=body)
    return [CustomerAPI(**i) for i in response.json()]

for i in api_get_appointments(min_date="2021-01-01", max_date="2021-11-20 "):
    print(f"{i.first_name} - {i.last_name} - {i.phone} - {i.email} - {i.appointment_datetime}  - {i.appointment_id} ")



