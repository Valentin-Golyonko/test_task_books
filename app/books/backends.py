from .models import NotificationsModel


def work_with_notifications(user, method: str, msg=''):
    if user.is_authenticated:
        if method == 'get':
            personal_msgs = NotificationsModel.objects.filter(sender=user, is_read=False)
            return [i.message for i in personal_msgs]
        elif method == 'set':
            ntf = NotificationsModel(sender=user, message=msg)
            ntf.save()
        elif method == 'count':
            return NotificationsModel.objects.filter(sender=user, is_read=False).count()
    else:
        pass
