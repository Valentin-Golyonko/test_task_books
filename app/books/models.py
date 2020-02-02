from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models

UserModel = get_user_model()


class RegisterUser(models.Model):
    """
    Регистрация
    1.1 Обязательные поля email, имя, фамилия, номер телефона
    1.2 Необязательные поля адрес, город
    1.3 После регистрации асинхронно выслать email с паролем
    """
    # user = models.OneToOneField(UserModel, on_delete=models.CASCADE, blank=False, null=False)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    email = models.EmailField(max_length=30, blank=False, null=False)
    phone_number = models.CharField(max_length=20, blank=False, null=False)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
