from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import RegisterForm
from .tasks import send_email


class BooksMainPage(TemplateView):
    template_name = 'books/books_main_page.html'

    def get(self, request, *args, **kwargs):
        response = {}
        return render(request=request, template_name=self.template_name, context=response)

    def post(self, request):
        print("BooksMainPage.POST:", request.POST)
        pass


class RegisterPage(TemplateView):
    template_name = 'books/register_page.html'

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request=request, template_name=self.template_name, context={'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            auth_user = form.save(commit=False)
            send_email.delay(str(auth_user.email))
            auth_user.save()
        else:
            print('! Error in Registration form validation !')

        return redirect(to='main-page')
