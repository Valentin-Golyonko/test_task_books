from django.conf.urls import include
from django.urls import path

from .views import (BooksMainPage, SignUpPage, LogInPage, TySignUpPage,
                    BookStatisticPage, NotificationPage, search_page, logout_user,
                    ExportBooksPage, BooksList)

urlpatterns = [
    path('', BooksMainPage.as_view(), name='main-page'),
    path('api-auth/', include('rest_framework.urls')),
    path('signup/', SignUpPage.as_view(), name='signup'),
    path('login/', LogInPage.as_view(), name='login'),
    path('ty-signup/', TySignUpPage.as_view(), name='ty-signup'),
    path('statistics/', BookStatisticPage.as_view(), name='statistics'),
    path('notifications/', NotificationPage.as_view(), name='notifications'),
    path('search/<search_it>/', search_page, name='search'),
    path('logout/', logout_user, name='logout'),
    path('book-export/', ExportBooksPage.as_view(), name='book-export'),
    path('books-add/', BooksList.as_view(), name='books-add'),
]
