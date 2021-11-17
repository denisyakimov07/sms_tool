from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore


def test():
    # add_to_db_all_customers()
    print('dddddddddddddddddddddddddddddd')


#
# def start():
#
#     scheduler = BackgroundScheduler()
#     scheduler.add_jobstore(DjangoJobStore(), "default")
#     scheduler.add_job(test, 'interval', seconds=220, id="worker1" , replace_existing=True)
#     scheduler.start()