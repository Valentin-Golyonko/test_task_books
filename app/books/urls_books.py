from django.urls import path
from django.conf.urls import include

from .views import BooksMainPage, RegisterPage

urlpatterns = [
    path('', BooksMainPage.as_view(), name='main-page'),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', RegisterPage.as_view(), name='auth'),
]
