from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import SignUpForm


class BooksMainPage(TemplateView):
    template_name = 'books/books_main_page.html'

    def get(self, request, *args, **kwargs):
        response = {}
        return render(request=request, template_name=self.template_name, context=response)

    def post(self, request):
        print("BooksMainPage.POST:", request.POST)
        pass


class RegisterPage(TemplateView):
    template_name = 'books/sign_up_page.html'

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request=request, template_name=self.template_name, context={'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user_password = '1234567890'
            user_email = form.cleaned_data.get('email')
            # send_email.delay(user_email, user_password)

            user = authenticate(request, username=username, password=user_password)
            login(request, user)
            print('login - OK')
        else:
            print('! Error in Registration form validation !')
        return redirect(to='main-page')


class LogInPage(TemplateView):
    template_name = 'books/login.html'

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request=request, template_name=self.template_name, context={'form': form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print('login - OK')
            return redirect(to='main-page')
        else:
            print('invalid login')
            return redirect(to='signup')


class SomeClass(TemplateView):
    @login_required(login_url='signin/')
    def get(self, request, *args, **kwargs):
        pass
