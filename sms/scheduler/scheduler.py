from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore



# This is the function you want to schedule - add as many as you want and then register them in the start() function below
import sms.views
from setup import update_appointments_interval
from sms import views


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # run this job every 24 hours
    # update dates in exist customer if not creat new one
    scheduler.add_job(views.update_appointments_for_two_last_days,
                      'interval',
                      seconds=update_appointments_interval,
                      id="update_appointments_for_two_last_days",
                      replace_existing=True)

    scheduler.start()
    # print("Scheduler started...", file=sys.stdout)