import datetime

import pytz

import setup

# Create your views here.
import acuityscheduling_API
from sms.models import Customer, CustomerAPI



from django.utils import timezone
datetime_now = timezone.now()



def get_customer_by_phone(phone):
    return Customer.objects.filter(phone_number=phone)




def add_to_db_all_customers():
    for api_customer in acuityscheduling_API.api_get_appointments():
        customer_from_db = get_customer_by_phone(phone=api_customer.phone)

        #if not customer in db -> creat
        if len(customer_from_db) == 0:
            new_customer = Customer()
            new_customer.first_name = api_customer.first_name
            new_customer.last_name = api_customer.last_name
            new_customer.phone_number = api_customer.phone
            new_customer.email = api_customer.email
            new_customer.last_appointment_id = api_customer.appointment_id
            new_customer.last_appointment_date = api_customer.appointment_datetime

            if api_customer.appointment_datetime >= datetime_now - datetime.timedelta(setup.days_for_old_customers):
                new_customer.warning_sms_date = api_customer.appointment_datetime + datetime.timedelta(334)
                new_customer.first_sms_date = api_customer.appointment_datetime + datetime.timedelta(344)
                new_customer.second_sms_date = api_customer.appointment_datetime + datetime.timedelta(351)
                new_customer.third_sms_date = api_customer.appointment_datetime + datetime.timedelta(358)
                new_customer.one_year_sms_date = api_customer.appointment_datetime + datetime.timedelta(365)
                new_customer.final_warning_7_days_sms_date = api_customer.appointment_datetime + datetime.timedelta(372)
            else:
                new_customer.warning_sms_date = datetime_now + datetime.timedelta(1)
                new_customer.first_sms_date = datetime_now + datetime.timedelta(7)
                new_customer.second_sms_date = datetime_now + datetime.timedelta(14)
                new_customer.third_sms_date = datetime_now + datetime.timedelta(21)
                new_customer.one_year_sms_date = datetime_now + datetime.timedelta(28)
                new_customer.final_warning_7_days_sms_date = datetime_now + datetime.timedelta(35)
            new_customer.save()

        else:
            #if exist update appointment date for newest

            if customer_from_db[0].last_appointment_date < api_customer.appointment_datetime:
                customer_from_db[0].last_appointment_date = api_customer.appointment_datetime
                customer_from_db[0].save()

            if api_customer.appointment_datetime > datetime_now - datetime.timedelta(setup.days_for_old_customers):
                customer_from_db[0].last_appointment_date = api_customer.appointment_datetime
                customer_from_db[0].warning_sms_date = api_customer.appointment_datetime + datetime.timedelta(setup.warning_sms_date_setup)
                customer_from_db[0].first_sms_date = api_customer.appointment_datetime + datetime.timedelta(setup.first_sms_date_setup)
                customer_from_db[0].second_sms_date = api_customer.appointment_datetime + datetime.timedelta(setup.second_sms_date_setup)
                customer_from_db[0].third_sms_date = api_customer.appointment_datetime + datetime.timedelta(setup.third_sms_date)
                customer_from_db[0].one_year_sms_date = api_customer.appointment_datetime + datetime.timedelta(setup.one_year_sms_date)
                customer_from_db[0].final_warning_7_days_sms_date = api_customer.appointment_datetime + datetime.timedelta(setup.final_warning_7_days_sms)
                customer_from_db[0].save()







# update dates in exist customer if not creat new one
def update_appointments_for_two_last_days():
    pass
    new_appointments: list[CustomerAPI] = acuityscheduling_API.api_get_appointments(min_date=datetime_now
                                                       - datetime.timedelta(setup.days_to_update_appointments))
    for dd in new_appointments:
        print(dd.phone)


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

                    customer_from_db[0].third_sms_date = customer.appointment_datetime + datetime.timedelta(
                        setup.third_sms_date)
                    customer_from_db[0].one_year_sms_date = customer.appointment_datetime + datetime.timedelta(
                        setup.one_year_sms_date)
                    customer_from_db[0].final_warning_7_days_sms_date = customer.appointment_datetime + datetime.timedelta(
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