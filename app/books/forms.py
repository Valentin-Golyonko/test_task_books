from django import forms

from .models import Profile


class SignUpForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'phone',
                  'address', 'city',)
