import datetime
import setup
import pytz

from django.utils import timezone


# Create your views here.
import acuityscheduling_API
from sms.models import Customer, CustomerAPI


def get_customer_by_phone(phone):
    return Customer.objects.filter(phone_number=phone)

def create_customer(customer: CustomerAPI):
    if customer.appointment_datetime <= timezone.now() - datetime.timedelta(setup.days_for_old_customers):
        new_customer = Customer()
        new_customer.first_name = customer.first_name
        new_customer.last_name = customer.last_name
        new_customer.phone_number = customer.phone
        new_customer.email = customer.email
        new_customer.last_appointment_id = customer.appointment_id

        new_customer.last_appointment_date = customer.appointment_datetime
        new_customer.warning_sms_date = timezone.now() + datetime.timedelta(1)
        new_customer.first_sms_date = timezone.now() + datetime.timedelta(8)
        new_customer.second_sms_date = timezone.now() + datetime.timedelta(14)
        new_customer.third_sms_date = timezone.now() + datetime.timedelta(21)
        new_customer.one_year_sms_date = timezone.now() + datetime.timedelta(28)
        new_customer.final_warning_7_days_sms_date = timezone.now() + datetime.timedelta(35)
        new_customer.save()
    else:
        new_customer = Customer()
        new_customer.first_name = customer.first_name
        new_customer.last_name = customer.last_name
        new_customer.phone_number = customer.phone
        new_customer.email = customer.email
        new_customer.last_appointment_id = customer.appointment_id
        new_customer.last_appointment_date = customer.appointment_datetime
        new_customer.warning_sms_date = customer.appointment_datetime + datetime.timedelta(setup.warning_sms_date_setup)
        new_customer.first_sms_date = customer.appointment_datetime + datetime.timedelta(setup.first_sms_date_setup)
        new_customer.second_sms_date = customer.appointment_datetime + datetime.timedelta(setup.second_sms_date_setup)
        new_customer.third_sms_date = customer.appointment_datetime + datetime.timedelta(setup.third_sms_date)
        new_customer.one_year_sms_date = customer.appointment_datetime + datetime.timedelta(setup.one_year_sms_date)
        new_customer.final_warning_7_days_sms_date = customer.appointment_datetime + datetime.timedelta(
            setup.final_warning_7_days_sms)
        new_customer.save()

def add_to_db_all_customers():
    for i in acuityscheduling_API.api_get_appointments():
        customer_from_db = get_customer_by_phone(phone=i.phone)
        if len(customer_from_db) == 0:
            create_customer(i)
        else:
            update_customers_dates(customer=customer_from_db[0], new_customer=i)

def update_customers_dates(customer: Customer, new_customer: CustomerAPI):
    if new_customer.appointment_datetime > customer.last_appointment_date:
        customer.last_appointment_date = new_customer.appointment_datetime
        customer.warning_sms_date = new_customer.appointment_datetime + datetime.timedelta(setup.warning_sms_date_setup)
        customer.first_sms_date = new_customer.appointment_datetime + datetime.timedelta(setup.first_sms_date_setup)
        customer.second_sms_date = new_customer.appointment_datetime + datetime.timedelta(setup.second_sms_date_setup)
        customer.third_sms_date = new_customer.appointment_datetime + datetime.timedelta(setup.third_sms_date)
        customer.one_year_sms_date = new_customer.appointment_datetime + datetime.timedelta(setup.one_year_sms_date)
        customer.final_warning_7_days_sms_date = new_customer.appointment_datetime + datetime.timedelta(setup.final_warning_7_days_sms)


        customer.save()





# update dates in exist customer if not creat new one
def update_appointments_for_two_last_days():
    new_appointments: list[CustomerAPI] = acuityscheduling_API.api_get_appointments(min_date=datetime.datetime.now()
                                                       - datetime.timedelta(setup.days_to_update_appointments))
    if len(new_appointments) >0:
        for customer in new_appointments:
            customer_from_db: list[Customer] = Customer.objects.filter(phone_number=customer.phone)
            if len(customer_from_db) > 0:
                if customer_from_db[0].last_appointment_date < customer.appointment_datetime:
                    customer_from_db[0].last_appointment_date = customer.appointment_datetime
                    customer_from_db[0].last_appointment_id = customer.appointment_id

                    customer_from_db[0].warning_sms_date = \
                        customer.appointment_datetime + datetime.timedelta(setup.warning_sms_date_setup)

                    customer_from_db[0].first_sms_date = \
                        customer.appointment_datetime + datetime.timedelta(setup.first_sms_date_setup)

                    customer_from_db[0].second_sms_date = \
                        customer.appointment_datetime + datetime.timedelta(setup.second_sms_date_setup)

                    customer_from_db[0].seven_days_sms = customer.appointment_datetime + datetime.timedelta(
                        setup.third_sms_date)
                    customer_from_db[0].zero_days_sms = customer.appointment_datetime + datetime.timedelta(
                        setup.one_year_sms_date)
                    customer_from_db[0].final_warning_7_days_sms = customer.appointment_datetime + datetime.timedelta(
                        setup.final_warning_7_days_sms)




                    customer_from_db[0].save()
                    print(f"{customer_from_db[0].phone_number} - updated successfully")
            else:
                new_customer = Customer()
                new_customer.first_name = customer.first_name
                new_customer.last_name = customer.last_name
                new_customer.phone_number = customer.phone
                new_customer.email = customer.email
                new_customer.last_appointment_id = customer.appointment_id
                new_customer.last_appointment_date = customer.appointment_datetime
                new_customer.warning_sms_date = customer.appointment_datetime + datetime.timedelta(
                    setup.warning_sms_date_setup)
                new_customer.first_sms_date = customer.appointment_datetime + datetime.timedelta(
                    setup.first_sms_date_setup)
                new_customer.second_sms_date = customer.appointment_datetime + datetime.timedelta(
                    setup.second_sms_date_setup)
                new_customer.save()


















