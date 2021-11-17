import datetime
import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from sms import acuityscheduling_API, setup

from sms.models import Customer

from django.utils import timezone
datetime_now = timezone.now()

def get_customer_by_phone(phone):
    return Customer.objects.filter(phone_number=phone)


# # update dates in exist customer if not creat new one
def update_appointments_for_two_last_days():
    new_appointments: list[Customer] = acuityscheduling_API.api_get_appointments(min_date=datetime_now
                                                                                          - datetime.timedelta(
        setup.days_to_update_appointments),
                                                                                 max_date=datetime_now + datetime.timedelta(60))

    if len(new_appointments) >0:
        for customer in new_appointments:
            customer_from_db: list[Customer] = Customer.objects.filter(phone_number=customer.phone_number)
            if len(customer_from_db) > 0:
                if customer_from_db[0].last_appointment_date < customer.last_appointment_date:
                    customer_from_db[0].last_appointment_date = customer.last_appointment_date
                    customer_from_db[0].last_appointment_id = customer.last_appointment_id
                    customer_from_db[0].warning_sms_date = \
                        customer.last_appointment_date + datetime.timedelta(setup.warning_sms_date_setup)
                    customer_from_db[0].first_sms_date = \
                        customer.last_appointment_date + datetime.timedelta(setup.first_sms_date_setup)
                    customer_from_db[0].second_sms_date = \
                        customer.last_appointment_date + datetime.timedelta(setup.second_sms_date_setup)
                    customer_from_db[0].third_sms_date = customer.last_appointment_date + datetime.timedelta(
                        setup.third_sms_date)
                    customer_from_db[0].one_year_sms_date = customer.last_appointment_date + datetime.timedelta(
                        setup.one_year_sms_date)
                    customer_from_db[0].final_warning_7_days_sms_date = customer.last_appointment_date + datetime.timedelta(
                        setup.final_warning_7_days_sms)

                    customer_from_db[0].save()
                    print(f"{customer_from_db[0].phone_number} - updated successfully")
            else:
                new_customer = Customer()
                new_customer.first_name = customer.first_name
                new_customer.last_name = customer.last_name
                new_customer.phone_number = customer.phone_number
                new_customer.email = customer.email
                new_customer.last_appointment_id = customer.last_appointment_id
                new_customer.last_appointment_date = customer.last_appointment_date

                new_customer.warning_sms_date = customer.last_appointment_date + datetime.timedelta(
                    setup.warning_sms_date_setup)

                new_customer.first_sms_date = customer.last_appointment_date + datetime.timedelta(
                    setup.first_sms_date_setup)

                new_customer.second_sms_date = customer.last_appointment_date + datetime.timedelta(
                    setup.second_sms_date_setup)

                new_customer.third_sms_date = customer.last_appointment_date + datetime.timedelta(
                    setup.third_sms_date)

                new_customer.one_year_sms_date = customer.last_appointment_date + datetime.timedelta(
                    setup.one_year_sms_date)

                new_customer.final_warning_7_days_sms = customer.last_appointment_date + datetime.timedelta(
                    setup.final_warning_7_days_sms)

                new_customer.save()


@csrf_exempt
def read_sms_from_customer(request):
    if request.method == 'POST':
        print(request.POST)
        # payload = json.loads(request.body)
        # print(payload)
        return JsonResponse({'test':1}, safe=False)