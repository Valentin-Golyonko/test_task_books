from django import forms

from .models import RegisterUser


class RegisterForm(forms.ModelForm):
    class Meta:
        model = RegisterUser
        fields = ['first_name', 'last_name', 'email',
                  'phone_number', 'address', 'city']
