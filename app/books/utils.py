from django.contrib import messages
from rest_framework.views import exception_handler

from .models import Notification


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code
        print("response: %s;\nException: %s" % (response, exc))
        errors = "response: %s;\nException: %s" % (response, exc)
        work_with_notifications(context['request'].user, 'set', 'Error in Add Book. %s' % errors)
        messages.error(context['request'], 'Error in Add Book %s' % errors)

    return response


def work_with_notifications(user, method: str, msg=''):
    if user.is_authenticated:
        if method == 'get':
            personal_msgs = Notification.objects.filter(sender=user, is_read=False)
            return [i.message for i in personal_msgs]
        elif method == 'set':
            ntf = Notification(sender=user, message=msg)
            ntf.save()
        elif method == 'count':
            return Notification.objects.filter(sender=user, is_read=False).count()
    else:
        pass
