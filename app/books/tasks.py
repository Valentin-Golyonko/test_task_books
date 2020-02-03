from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_email(username: str, user_email: str, password: str):
    # print('user_email: %s, password: %s' % (user_email, password))

    subject = 'Django site Registering'
    message = 'Hello, %s! Thank you for registering to our site. ' \
              'It  means a world to us, ' \
              'your password is: %s' % (username, password)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email, ]
    send_mail(subject, message, email_from, recipient_list)

    return 'send_email - OK'
