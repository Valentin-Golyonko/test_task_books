from django.urls import path
from django.conf.urls import include
from django.contrib.auth.views import LoginView

from .views import BooksMainPage, RegisterPage, LogInPage

urlpatterns = [
    path('', BooksMainPage.as_view(), name='main-page'),
    path('api-auth/', include('rest_framework.urls')),
    path('signup/', RegisterPage.as_view(), name='signup'),
    path('login/', LogInPage.as_view(), name='signin'),
]
