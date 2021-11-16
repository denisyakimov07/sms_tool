import csv
import datetime

from acuityscheduling_API import api_get_appointments
from sms.models import Customer
from sms.views import datetime_now, get_customer_by_phone


def one_time_load_all_customers():
    cus_list =  api_get_appointments(min_date=datetime.datetime.strptime("2019-01-01", "%Y-%m-%d"),
                                     max_date=datetime.datetime.strptime("2019-08-01", "%Y-%m-%d"))
    add_to_db_all_customers(cus_list)

    cus_list = api_get_appointments(min_date=datetime.datetime.strptime("2019-08-01", "%Y-%m-%d"),
                                    max_date=datetime.datetime.strptime("2019-12-31", "%Y-%m-%d"))
    add_to_db_all_customers(cus_list)

    cus_list = api_get_appointments(min_date=datetime.datetime.strptime("2019-12-31", "%Y-%m-%d"),
                                    max_date=datetime.datetime.strptime("2020-06-01", "%Y-%m-%d"))
    add_to_db_all_customers(cus_list)

    cus_list = api_get_appointments(min_date=datetime.datetime.strptime("2020-06-01", "%Y-%m-%d"),
                                    max_date=datetime.datetime.strptime("2021-01-01", "%Y-%m-%d"))
    add_to_db_all_customers(cus_list)

    cus_list = api_get_appointments(min_date=datetime.datetime.strptime("2021-01-01", "%Y-%m-%d"),
                                    max_date=datetime.datetime.strptime("2021-06-01", "%Y-%m-%d"))
    add_to_db_all_customers(cus_list)

    cus_list = api_get_appointments(min_date=datetime.datetime.strptime("2021-06-01", "%Y-%m-%d"),
                                    max_date=datetime.datetime.strptime("2021-12-31", "%Y-%m-%d"))
    add_to_db_all_customers(cus_list)


def get_warning_sms_date_customers():
    s_data = datetime_now + datetime.timedelta(1)

    list = Customer.objects.filter(warning_sms_date__date=s_data)
    # print(f"{s_data}  --  {len(list)}")
    print(len(list))

def first_sms_date():
    s_data = datetime_now + datetime.timedelta(1)

    list = Customer.objects.filter(first_sms_date=s_data)
        # print(f"{s_data}  --  {len(list)}")
    print(len(list))


def save_to_csv(customer_list: list[Customer]):
    # field names
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'last_appointment_date',
              'warning_sms_date', 'first_sms_date', 'second_sms_date', 'third_sms_date', 'one_year_sms_date',
              'final_warning_7_days_sms_date', 'last_appointment_id']
    # data rows of csv file
    customer_list_to_csv = []
    for customer in customer_list:
        customer_list_to_csv.append([customer.first_name, customer.last_name, customer.email, customer.phone_number,
                              customer.last_appointment_date, customer.warning_sms_date, customer.first_sms_date,
                              customer.second_sms_date, customer.third_sms_date, customer.one_year_sms_date,
                              customer.final_warning_7_days_sms_date, customer.last_appointment_id])
    # name of csv file
    filename = "university_records.csv"
    # writing to csv file
    with open(filename, 'w', encoding="utf-8") as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields)
        # writing the data rows
        csvwriter.writerows(customer_list_to_csv)

def update_2019():
    list = Customer.objects.filter(last_appointment_date__range=[datetime.datetime.strptime("2019-11-20", "%Y-%m-%d"),
                                                            datetime.datetime.strptime("2019-12-31", "%Y-%m-%d")])

    print(len(list))
    for customer in list:
        customer.warning_sms_date = customer.last_appointment_date + datetime.timedelta(334 + 365)
        customer.first_sms_date = customer.last_appointment_date + datetime.timedelta(344 + 365)
        customer.second_sms_date = customer.last_appointment_date + datetime.timedelta(351 + 365 )
        customer.third_sms_date = customer.last_appointment_date + datetime.timedelta(358 + 365 )
        customer.one_year_sms_date = customer.last_appointment_date + datetime.timedelta(365+ 365)
        customer.final_warning_7_days_sms_date = customer.last_appointment_date + datetime.timedelta(372+ 365)
        customer.save()


def update_2020():
    list = Customer.objects.filter(last_appointment_date__range=[datetime.datetime.strptime("2020-11-20", "%Y-%m-%d"),
                                                            datetime.datetime.strptime("2020-12-31", "%Y-%m-%d")])

    print(len(list))
    for customer in list:
        customer.warning_sms_date = customer.last_appointment_date + datetime.timedelta(334)
        customer.first_sms_date = customer.last_appointment_date + datetime.timedelta(344)
        customer.second_sms_date = customer.last_appointment_date + datetime.timedelta(351)
        customer.third_sms_date = customer.last_appointment_date + datetime.timedelta(358)
        customer.one_year_sms_date = customer.last_appointment_date + datetime.timedelta(365)
        customer.final_warning_7_days_sms_date = customer.last_appointment_date + datetime.timedelta(372)
        customer.save()
#

def add_to_db_all_customers(customers_from_api: list[Customer]):
    for customer_from_api in customers_from_api:
        customer_from_db = get_customer_by_phone(phone=customer_from_api.phone_number)

        #if not customer in db -> creat
        if len(customer_from_db) == 0:
            new_customer = Customer()
            new_customer.first_name = customer_from_api.first_name
            new_customer.last_name = customer_from_api.last_name
            new_customer.phone_number = customer_from_api.phone_number
            new_customer.email = customer_from_api.email
            new_customer.last_appointment_id = customer_from_api.last_appointment_id
            new_customer.last_appointment_date = customer_from_api.last_appointment_date

            if customer_from_api.last_appointment_date >= datetime_now - datetime.timedelta(setup.days_for_old_customers):
                new_customer.warning_sms_date = customer_from_api.last_appointment_date + datetime.timedelta(334)
                new_customer.first_sms_date = customer_from_api.last_appointment_date + datetime.timedelta(344)
                new_customer.second_sms_date = customer_from_api.last_appointment_date + datetime.timedelta(351)
                new_customer.third_sms_date = customer_from_api.last_appointment_date + datetime.timedelta(358)
                new_customer.one_year_sms_date = customer_from_api.last_appointment_date + datetime.timedelta(365)
                new_customer.final_warning_7_days_sms_date = customer_from_api.last_appointment_date + datetime.timedelta(372)
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

            if customer_from_db[0].last_appointment_date < customer_from_api.last_appointment_date:
                customer_from_db[0].last_appointment_date = customer_from_api.last_appointment_date
                customer_from_db[0].save()

            if customer_from_api.last_appointment_date > datetime_now - datetime.timedelta(setup.days_for_old_customers):
                customer_from_db[0].warning_sms_date = customer_from_api.last_appointment_date + datetime.timedelta(setup.warning_sms_date_setup)
                customer_from_db[0].first_sms_date = customer_from_api.last_appointment_date + datetime.timedelta(setup.first_sms_date_setup)
                customer_from_db[0].second_sms_date = customer_from_api.last_appointment_date + datetime.timedelta(setup.second_sms_date_setup)
                customer_from_db[0].third_sms_date = customer_from_api.last_appointment_date + datetime.timedelta(setup.third_sms_date)
                customer_from_db[0].one_year_sms_date = customer_from_api.last_appointment_date + datetime.timedelta(setup.one_year_sms_date)
                customer_from_db[0].final_warning_7_days_sms_date = customer_from_api.last_appointment_date + datetime.timedelta(setup.final_warning_7_days_sms)
                customer_from_db[0].save()



def add_data_from_file():
    reader = csv.DictReader(open('sms_customer.csv'))

    for i in reader:
        cust = Customer()
        cust.first_name = i['first_name']
        cust.last_name = i['last_name']
        cust.email = i['email']
        cust.phone_number = i['phone_number']
        cust.last_appointment_id = i['last_appointment_id']
        cust.last_appointment_date = i['last_appointment_date']
        cust.warning_sms_date = i['warning_sms_date']
        cust.first_sms_date = i['first_sms_date']
        cust.second_sms_date = i['second_sms_date']
        cust.third_sms_date = i['third_sms_date']
        cust.one_year_sms_date = i['one_year_sms_date']
        cust.final_warning_7_days_sms_date = i['final_warning_7_days_sms_date']
        cust.cancel_by_customer = False
        cust.save()