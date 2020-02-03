from celery import shared_task


@shared_task
def send_email(user_email: str, password: str):
    print('user_email:', user_email, 'password:', password)

    return 'Done!'
