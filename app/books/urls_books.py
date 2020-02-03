from django.conf.urls import include
from django.urls import path

from .views import (BooksMainPage, SignUpPage, LogInPage, TySignUpPage)

urlpatterns = [
    path('', BooksMainPage.as_view(), name='main-page'),
    path('api-auth/', include('rest_framework.urls')),
    path('signup/', SignUpPage.as_view(), name='signup'),
    path('login/', LogInPage.as_view(), name='login'),
    path('ty-signup/', TySignUpPage.as_view(), name='ty-signup'),
]
