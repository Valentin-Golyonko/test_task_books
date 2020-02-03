from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=50, required=True)
    phone = forms.CharField(max_length=20, required=True)
    address = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone',
                  'address', 'city',)
        exclude = ('password1', 'password2',)
