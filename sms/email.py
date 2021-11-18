import smtplib
from email.message import EmailMessage

from environment import get_env
from sms.models import ReportRecipient


def send_email(msg):



    emails = ReportRecipient.objects.all()

    for email in emails:
        try:
            destination = email.email
            from_whom = "Daily report Bot"
            subject = "Daily report"
            to_send = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (from_whom, destination, subject, msg)

            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(get_env().MAIL_USERNAME, get_env().MAIL_PASSWORD)

            server.sendmail(get_env().MAIL_USERNAME, email.email, to_send)
            server.quit()
        except Exception as e:
            print(e)



