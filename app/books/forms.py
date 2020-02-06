from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import (Profile, BooksModel)


class SignUpForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'phone',
                  'address', 'city',)


class LogInForm(forms.Form):
    email_address = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(max_length=50, required=True, )

    class Meta(AuthenticationForm):
        fields = ('email_address', 'password',)


class AddBookForm(forms.ModelForm):
    class Meta:
        model = BooksModel
        fields = ('title', 'author', 'isbn',)
