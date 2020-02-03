from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import (SignUpForm, LogInForm)
from .tasks import send_email


class BooksMainPage(TemplateView):
    template_name = 'books/books_main_page.html'

    def get(self, request, *args, **kwargs):
        response = {}
        return render(request=request, template_name=self.template_name, context=response)

    def post(self, request):
        print("BooksMainPage.POST:", request.POST)
        pass


class SignUpPage(TemplateView):
    template_name = 'books/sign_up_page.html'

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request=request, template_name=self.template_name, context={'form': form})

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

            # send_email.delay(user_first_name, user_email, user_password)
            print('username: %s, user_email: %s, password: %s' % (user_first_name,
                                                                  user_email, user_password))

            return redirect(to='ty-signup')
        else:
            print('! Error in Registration form validation !')
        return redirect(to='signup')


class LogInPage(TemplateView):
    template_name = 'books/login.html'

    def get(self, request, *args, **kwargs):
        form = LogInForm()
        return render(request=request, template_name=self.template_name, context={'form': form})

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
        response = {}
        return render(request=request, template_name=self.template_name, context=response)


class SomeClass(TemplateView):
    @login_required(login_url='signin/')
    def get(self, request, *args, **kwargs):
        pass
