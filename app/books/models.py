from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.db import models

UserModel = get_user_model()


class Profile(models.Model):
    """
    Регистрация
    1.1 Обязательные поля email, имя, фамилия, номер телефона
    1.2 Необязательные поля адрес, город
    1.3 После регистрации асинхронно выслать email с паролем
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    email = models.EmailField(max_length=30, blank=False, null=False, unique=True)
    phone = models.CharField(max_length=20, blank=False, null=False)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
