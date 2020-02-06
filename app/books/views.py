import csv
from datetime import date

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from rest_framework import authentication, permissions, generics

from .backends import work_with_notifications
from .forms import (SignUpForm, LogInForm)
from .models import (BooksModel, BooksSalesModel, AuthorModel, NotificationsModel)
from .serializers import BooksSerializer
from .tasks import send_email


class BooksMainPage(TemplateView):
    """ 3.2 Список книг """
    template_name = 'books/books_main_page.html'

    def get(self, request, *args, **kwargs):
        books = BooksModel.objects.all()
        paginator = Paginator(books, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        response = {'page_obj': page_obj,
                    'messages': get_messages(request),
                    'msg_count': work_with_notifications(request.user, 'count'),
                    'is_authed': int(request.user.is_authenticated),
                    }
        return render(request=request, template_name=self.template_name, context=response)

    def post(self, request):
        data_to_search = request.POST['input_search']
        return redirect(to='search', search_it=data_to_search)


class SignUpPage(TemplateView):
    template_name = 'books/sign_up_page.html'

    def get(self, request, *args, **kwargs):
        response = {'form': SignUpForm(),
                    'messages': get_messages(request),
                    'is_authed': int(request.user.is_authenticated),
                    }
        return render(request=request, template_name=self.template_name, context=response)

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)
            user_first_name = form.cleaned_data.get('first_name')
            user_password = User.objects.make_random_password()
            user_email = form.cleaned_data.get('email')

            create_user = User.objects.create_user(username=user_first_name,
                                                   first_name=user_first_name,
                                                   last_name=form.cleaned_data.get('last_name'),
                                                   email=user_email,
                                                   password=user_password)
            create_user.save()

            user_form.user = create_user
            user_form.save()

            """ - После регистрации асинхронно выслать email с паролем """
            send_email.delay(user_first_name, user_email, user_password)

            messages.success(request, 'Registration success!')
            return redirect(to='ty-signup')
        else:
            messages.error(request, 'Error in Registration form validation!')
        return redirect(to='signup')


class LogInPage(TemplateView):
    """ Логин по email, password """
    template_name = 'books/login.html'

    def get(self, request, *args, **kwargs):
        response = {'form': LogInForm(),
                    'messages': get_messages(request),
                    'is_authed': int(request.user.is_authenticated),
                    }
        return render(request=request, template_name=self.template_name, context=response)

    def post(self, request):
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email_address')
            password = form.cleaned_data.get('password')
            try:
                get_username = User.objects.get(email=email)
            except Exception as ex:
                print('! Error in User email) !\n%s' % ex)
                messages.error(request, 'Email is wrong!')
                return redirect(to='login')
            else:
                user = authenticate(request, username=get_username.username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Login success!')
                    work_with_notifications(request.user, 'set', 'Login success!')
                    return redirect(to='main-page')
                else:
                    messages.error(request, 'Invalid Password!')
                    return redirect(to='login')
        else:
            messages.error(request, 'Error in Login form validation!')
            return redirect(to='login')


class TySignUpPage(TemplateView):
    template_name = 'books/ty_for_signup.html'

    def get(self, request, *args, **kwargs):
        return render(request=request, template_name=self.template_name,
                      context={'messages': get_messages(request),
                               'is_authed': int(request.user.is_authenticated), })


class BookStatisticPage(TemplateView):
    """ 3.1 Статистика """
    template_name = 'books/books_statistic.html'

    def get(self, request, *args, **kwargs):
        """ - Книг продано всего """
        books_sales = BooksSalesModel.objects.all()
        total_sales = books_sales.aggregate(Sum('sales'))['sales__sum']

        """ - Книг продано за прошлый месяц """
        months = [i for i in range(1, 13)]
        month_now = date.today().month
        sales_last_month = books_sales.filter(
            sold_day__month=months[month_now - 2]).aggregate(Sum('sales'))['sales__sum']

        books_total = BooksModel.objects.all()

        """ - Продано книг по авторам (%) """
        author_data = []
        if total_sales:
            authors = AuthorModel.objects.all()
            for author in authors:
                author_books = books_total.filter(author=author)
                author_sales = 0
                for book in author_books:
                    sales__sum = books_sales.filter(book=book).aggregate(Sum('sales'))
                    if any(sales__sum.values()):
                        author_sales += sales__sum['sales__sum']
                author_sales_percent = round(100 * (author_sales / total_sales), 2)
                author_data.append([author.author_name, author_sales_percent])

        author_data.sort(key=lambda s: s[1], reverse=True)

        """ - Продано книг  """
        books_sold = 0
        for book in books_total:
            is_sold = books_sales.filter(book=book)
            if any(is_sold):
                books_sold += 1
        all_books = books_total.count()
        if all_books:
            sold_vs_all_books = round(100 * (books_sold / all_books), 2)
        else:
            sold_vs_all_books = 0

        response = {'total_sales': total_sales,
                    'sales_last_month': sales_last_month,
                    'author_data': author_data,
                    'books_sold': books_sold,
                    'all_books': all_books,
                    'sold_vs_all_books': sold_vs_all_books,
                    'msg_count': work_with_notifications(request.user, 'count'),
                    'is_authed': int(request.user.is_authenticated),
                    }
        return render(request=request, template_name=self.template_name, context=response)


def search_page(request, search_it):
    """ - Общий фильтр по названию книги, имени автора, артикулу """
    if request.method == 'GET':
        work_with_notifications(request.user, method='set', msg="search: %s" % search_it)

        data = {'found_books': BooksModel.objects.filter(title__contains=search_it),
                'found_authors': AuthorModel.objects.filter(author_name__contains=search_it),
                'found_isbn': BooksModel.objects.filter(isbn__contains=search_it),
                'search_it': search_it,
                'msg_count': work_with_notifications(request.user, 'count'),
                'is_authed': int(request.user.is_authenticated),
                }
        return render(request=request, template_name='books/book_search.html', context=data)


class NotificationPage(TemplateView):
    """ - Персональные нотификации. Выводить не больше 5 ранее виденных.
    Выделить впервые увиденные нотификации
    """
    template_name = 'books/books_notification.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_msg = work_with_notifications(request.user, 'get')
            NotificationsModel.objects.filter(sender=request.user, is_read=False).update(is_read=True)

            old_notif = NotificationsModel.objects.filter(sender=request.user, is_read=True)
            msg_old_5 = [i.message for i in old_notif[:5]]

            response = {'user_msg': user_msg,
                        'user': request.user,
                        'msg_old_5': msg_old_5,
                        'is_authed': 1,
                        }
        else:
            response = {}
        return render(request=request, template_name=self.template_name, context=response)


def logout_user(request):
    logout(request)
    return redirect(to='main-page')


class ExportBooksPage(TemplateView):
    template_name = 'books/books_export.html'

    def get(self, request, *args, **kwargs):
        response = {'is_authed': int(request.user.is_authenticated), }
        return render(request=request, template_name=self.template_name, context=response)

    def post(self, request):
        if request.user.is_authenticated:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="books.csv"'
            writer = csv.writer(response)

            books_all = BooksModel.objects.all()
            for book in books_all:
                authors = [i.author_name for i in book.author.all()]
                writer.writerow([book.title, ', '.join(authors)])

            return response
        else:
            return JsonResponse({'redirect': '/login/'})


class BooksList(generics.ListCreateAPIView):
    queryset = BooksModel.objects.all()
    serializer_class = BooksSerializer

    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        work_with_notifications(request.user, 'set', 'You created a book.')
        return redirect(to='main-page')
