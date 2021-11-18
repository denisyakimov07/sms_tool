import smtplib

from environment import get_env


def send_email(msg):
    subject = "Weekly Report"
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(get_env().MAIL_USERNAME, get_env().MAIL_PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(get_env().MAIL_USERNAME, get_env().MAIL_USERNAME, message)
        server.quit()
    except Exception as e:
        print(e)



