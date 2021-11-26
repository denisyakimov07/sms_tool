from loguru import logger

import datetime

from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from environment import get_env
from sms import acuityscheduling_API, setup

from sms.models import Customer, MainSetup

from django.utils import timezone

from sms.my_logger import unsubscribe_customer_log, daily_report
from sms.twilio import send_sms_to_customer

import threading

def get_customer_by_phone(phone):
    return Customer.objects.filter(phone_number=phone)


# # update dates in exist customer if not creat new one
def update_app():
    try:
        new_appointments: list[Customer] = acuityscheduling_API.api_get_appointments(min_date=timezone.now()
                                                                                              - datetime.timedelta(
            setup.days_to_update_appointments), max_date=timezone.now() + datetime.timedelta(60))
        if len(new_appointments) > 0:
            for customer in new_appointments:
                customer_from_db: list[Customer] = Customer.objects.filter(phone_number=customer.phone_number)
                if len(customer_from_db) > 0:
                    if customer_from_db[0].last_appointment_date < customer.last_appointment_date:
                        customer_from_db[0].last_appointment_date = customer.last_appointment_date
                        customer_from_db[0].last_appointment_id = customer.last_appointment_id
                        customer_from_db[0].warning_sms_date = \
                            customer.last_appointment_date + datetime.timedelta(setup.warning_sms_date_setup)
                        customer_from_db[0].second_sms_date = \
                            customer.last_appointment_date + datetime.timedelta(setup.second_sms_date_setup)
                        customer_from_db[0].third_sms_date = customer.last_appointment_date + datetime.timedelta(
                            setup.third_sms_date)
                        customer_from_db[0].one_year_sms_date = customer.last_appointment_date + datetime.timedelta(
                            setup.one_year_sms_date)
                        customer_from_db[0].save()
                        logger.success(f"Successfully updated last appointments - {customer_from_db[0].phone_number}.")
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

                    new_customer.second_sms_date = customer.last_appointment_date + datetime.timedelta(
                        setup.second_sms_date_setup)

                    new_customer.third_sms_date = customer.last_appointment_date + datetime.timedelta(
                        setup.third_sms_date)

                    new_customer.one_year_sms_date = customer.last_appointment_date + datetime.timedelta(
                        setup.one_year_sms_date)
                    new_customer.save()
                    logger.success(f"Successfully created new customer - {new_customer.phone_number}.")
    except Exception as e:
        logger.error("ERROR: Can't update/create customer information")
        logger.trace(e)


def redirect_view(request):
    response = redirect('/admin/')
    return response


# subscription/unsubscribe process
@csrf_exempt
def read_sms_from_customer(request):
    if request.method == 'POST':
        try:
            phone_number = request.POST.get('From')
            sms_message = request.POST.get('Body')
            customer = Customer.objects.filter(phone_number__contains=phone_number[2:])
            if customer:
                customer = customer[0]
                logger.info(f"Customer message - {customer} - {sms_message}")
                if customer and 'stop' in str(sms_message).lower():
                    customer.cancel_by_customer = True
                    customer.save()
                    unsubscribe_customer_log(customer)
                    logger.success(f"Customer unsubscribe - {customer}")
                if customer and 'start' in str(sms_message).lower():
                    customer.cancel_by_customer = False
                    customer.save()
                    logger.success(f"Customer subscribe - {customer}")
            else:
                logger.warning(f"Can't find customer - {phone_number}")
            return HttpResponse(status=200)
        except Exception as e:
            logger.error(f"ERROR: Can't read post message")
            logger.trace(e)
            return HttpResponse(status=401)


def background_task():
    update_app()
    sent_customers_warning_sms_date_today()
    sent_customers_second_sms_date()
    sent_customers_third_sms_date()
    sent_customers_one_year_sms_date()
    daily_report()


@csrf_exempt
def scheduler(request):
    if request.method == 'POST' and request.POST.get('password') == get_env().SCHEDULER_KEY:
        try:
            threading.Thread(target=background_task).start()
            logger.success("Success scheduler task")
            return HttpResponse(status=200)
        except Exception as e:
            logger.error(f"ERROR: Daily task is fail.")
            logger.trace(e)
    else:
        return HttpResponse(status=401)


def sent_customers_warning_sms_date_today():
    try:
        customers_list = Customer.objects.filter(warning_sms_date__date=timezone.now(), cancel_by_customer=False)
        logger.info(f"Creat customers_warning_sms_date list - Length ({len(customers_list)}).")
    except Exception as e:
        logger.error(f"ERROR: Can't create warning_sms_date customers_list")
        logger.trace(e)
    try:
        send_sms_to_customer(customers_list=customers_list, sms_body=MainSetup.objects.first().warning_sms,
                             message_type="warning_sms_date")
    except Exception as e:
        logger.error(f"ERROR: Send sms to customer (warning_sms_date)")
        logger.trace(e)


def sent_customers_second_sms_date():
    try:
        customers_list = Customer.objects.filter(second_sms_date__date=timezone.now(), cancel_by_customer=False)
        logger.info(f"Creat customers second_sms list - Length ({len(customers_list)}).")
    except Exception as e:
        logger.error(f"ERROR: Can't create second_sms customers_list")
        logger.trace(e)
    try:
        send_sms_to_customer(customers_list=customers_list, sms_body=MainSetup.objects.first().second_sms_date,
                             message_type="second_sms_date")
    except Exception as e:
        logger.error(f"ERROR: Send sms to customer (second_sms)")
        logger.trace(e)


def sent_customers_third_sms_date():
    try:
        customers_list = Customer.objects.filter(third_sms_date__date=timezone.now(), cancel_by_customer=False)
        logger.info(f"Creat customers third_sms list - Length ({len(customers_list)}).")
    except Exception as e:
        logger.error(f"ERROR: Can't create third_sms customers_list")
        logger.trace(e)
    try:
        send_sms_to_customer(customers_list=customers_list, sms_body=MainSetup.objects.first().third_sms_date,
                             message_type="third_sms_date")
    except Exception as e:
        logger.error(f"ERROR: Send sms to customer (third_sms)")
        logger.trace(e)


def sent_customers_one_year_sms_date():
    try:
        customers_list = Customer.objects.filter(one_year_sms_date__date=timezone.now(), cancel_by_customer=False)
        logger.info(f"Creat customers one_year_sms list - Length ({len(customers_list)}).")
    except Exception as e:
        logger.error(f"ERROR: Can't create one_year_sms customers_list")
        logger.trace(e)
    try:
        send_sms_to_customer(customers_list=customers_list, sms_body=MainSetup.objects.first().one_year_sms_date,
                             message_type="one_year_sms_date")
    except Exception as e:
        logger.error(f"ERROR: Send sms to customer (one_year_sms)")
        logger.trace(e)


