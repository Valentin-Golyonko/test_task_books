from celery import shared_task


@shared_task
def send_email(user_email: str):
    print('user_email:', user_email)

    return 'Done!'
