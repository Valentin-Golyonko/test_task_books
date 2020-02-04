from datetime import date

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import (SignUpForm, LogInForm)
from .models import (BooksModel, BooksSalesModel, AuthorModel)
from .tasks import send_email


class BooksMainPage(TemplateView):
    """ 3.2 Список книг """
    template_name = 'books/books_main_page.html'

    def get(self, request, *args, **kwargs):
        books = BooksModel.objects.all()
        paginator = Paginator(books, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        response = {'page_obj': page_obj}
        return render(request=request, template_name=self.template_name, context=response)

    def post(self, request):
        data_to_search = request.POST['input_search']
        return redirect(to='search', search_it=data_to_search)


class SignUpPage(TemplateView):
    template_name = 'books/sign_up_page.html'

    def get(self, request, *args, **kwargs):
        return render(request=request, template_name=self.template_name,
                      context={'form': SignUpForm()})

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

            # print('username: %s, user_email: %s, password: %s' % (user_first_name,
            #                                                       user_email, user_password))
            """ - После регистрации асинхронно выслать email с паролем """
            send_email.delay(user_first_name, user_email, user_password)

            return redirect(to='ty-signup')
        else:
            print('! Error in Registration form validation !')
        return redirect(to='signup')


class LogInPage(TemplateView):
    """ Логин по email, password """
    template_name = 'books/login.html'

    def get(self, request, *args, **kwargs):
        return render(request=request, template_name=self.template_name,
                      context={'form': LogInForm()})

    def post(self, request):
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email_address')
            password = form.cleaned_data.get('password')
            try:
                get_username = User.objects.get(email=email)
            except Exception as ex:
                print('! Error in User.objects.get(email=email) !\n%s' % ex)
                return redirect(to='login')
            else:
                user = authenticate(request, username=get_username.username, password=password)
                if user is not None:
                    login(request, user)
                    print('login - OK')
                    return redirect(to='main-page')
                else:
                    print('! invalid login - ERROR')
                    return redirect(to='login')
        else:
            print('! Error in Login form validation !')
            return redirect(to='login')


class TySignUpPage(TemplateView):
    template_name = 'books/ty_for_signup.html'

    def get(self, request, *args, **kwargs):
        return render(request=request, template_name=self.template_name, context={})


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
                    }
        return render(request=request, template_name=self.template_name, context=response)


def search_page(request, search_it):
    """ - Общий фильтр по названию книги, имени автора, артикулу """
    if request.method == 'GET':
        found_books = BooksModel.objects.filter(title__contains=search_it)
        found_authors = AuthorModel.objects.filter(author_name__contains=search_it)
        found_isbn = BooksModel.objects.filter(isbn__contains=search_it)
        data = {'found_books': found_books,
                'found_authors': found_authors,
                'found_isbn': found_isbn,
                'search_it': search_it,
                }
        return render(request=request, template_name='books/book_search.html', context=data)


class NotificationPage(TemplateView):
    """ 3.3 Список нотификаций """
    template_name = 'books/books_notification.html'

    def get(self, request, *args, **kwargs):
        response = {}
        return render(request=request, template_name=self.template_name, context=response)


class SomeClass(TemplateView):
    @login_required(login_url='login/')
    def get(self, request, *args, **kwargs):
        pass
