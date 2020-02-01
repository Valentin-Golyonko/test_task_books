from django.views.generic import TemplateView

from .models import MyModel


class MyView(TemplateView):
    MyModel.objects.all()
