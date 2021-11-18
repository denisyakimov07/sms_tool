from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

from sms.my_logger import daily_report
from sms.views import update_app, sent_customers_warning_sms_date_today, sent_customers_first_sms_date, \
    sent_customers_second_sms_date, sent_customers_third_sms_date, sent_customers_one_year_sms_date, \
    sent_customers_final_warning_7_days_sms_date


def sent_sms():
    sent_customers_warning_sms_date_today()
    sent_customers_first_sms_date()
    sent_customers_second_sms_date()
    sent_customers_third_sms_date()
    sent_customers_one_year_sms_date()
    sent_customers_final_warning_7_days_sms_date()


def start():

    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(update_app, trigger='cron', hour="16", id="Update acuityscheduling appointments" , replace_existing=True)
    scheduler.add_job(daily_report, trigger='cron', hour="06", minute='00', id="Sent daily report" , replace_existing=True)
    scheduler.add_job(sent_sms, trigger='cron', hour="16", minute='05', id="Sent sms", replace_existing=True)

    scheduler.start()