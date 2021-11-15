from apscheduler.schedulers.background import BackgroundScheduler

from sms.views import add_to_db_all_customers


def test():
    # add_to_db_all_customers()
    print('dddddddddddddddddddddddddddddd')



def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(test, 'interval', seconds=120, id="worker1" , replace_existing=True)
    scheduler.start()