import datetime
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
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


def redirect_view(request):
    response = redirect('/admin/')
    return response

#subscription/unsubscribe procces
@csrf_exempt
def read_sms_from_customer(request):
    if request.method == 'POST':
        phone_number = request.POST.get('From')
        sms_message = request.POST.get('Body')
        customer = Customer.objects.filter(phone_number__contains=phone_number[2:])
        if customer:
            customer= customer[0]
            print(f"{customer} - {sms_message}")
            if customer and 'stop' in str(sms_message).lower():
                customer.cancel_by_customer = True
                customer.save()
            if customer and 'start' in str(sms_message).lower():
                customer.cancel_by_customer = False
                customer.save()
        else:
            print(f"Can't find {phone_number}")
        return JsonResponse({'test':1}, safe=False)


days =2

def get_customers_warning_sms_date_today():
    customers_list = Customer.objects.filter(warning_sms_date__date=datetime_now + datetime.timedelta(days), cancel_by_customer= False)
    print(datetime_now + datetime.timedelta(days))
    print(customers_list)
    for i in customers_list:
        print(i)
    print()

def get_customers_first_sms_date():
    customers_list = Customer.objects.filter(first_sms_date__date=datetime_now + datetime.timedelta(days), cancel_by_customer= False)
    print(customers_list)
    for i in customers_list:
        print(i)
    print()

def get_customers_second_sms_date():
    customers_list = Customer.objects.filter(second_sms_date__date=datetime_now + datetime.timedelta(days), cancel_by_customer= False)
    print(customers_list)
    for i in customers_list:
        print(i)
    print()

def get_customers_third_sms_date():
    customers_list = Customer.objects.filter(third_sms_date__date=datetime_now + datetime.timedelta(days), cancel_by_customer= False)
    print(customers_list)
    for i in customers_list:
        print(i)
    print()

def get_customers_one_year_sms_date():
    customers_list = Customer.objects.filter(one_year_sms_date__date=datetime_now + datetime.timedelta(days), cancel_by_customer= False)
    print(customers_list)
    for i in customers_list:
        print(i)
    print()

def get_customers_final_warning_7_days_sms_date():
    customers_list = Customer.objects.filter(final_warning_7_days_sms_date__date=datetime_now + datetime.timedelta(days), cancel_by_customer= False)
    print(customers_list)
    for i in customers_list:
        print(i)
    print()