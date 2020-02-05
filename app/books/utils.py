from django.contrib import messages
from rest_framework.views import exception_handler

from .backends import work_with_notifications


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code
        print("response: %s;\nException: %s" % (response, exc))
        errors = "response: %s;\nException: %s" % (response, exc)
        work_with_notifications(context['request'].user, 'set', 'Error in Add Book. %s' % errors)
        messages.error(context['request'], 'Error in Add Book %s' % errors)

    return response
