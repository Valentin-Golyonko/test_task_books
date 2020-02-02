from django.http import HttpResponse
from django.views.generic import TemplateView

from .models import MyModel


class MyView(TemplateView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello, world. You're at the polls index.")
