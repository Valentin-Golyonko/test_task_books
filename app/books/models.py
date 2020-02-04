from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.db import models


class ProfileModel(models.Model):
    """
    - Обязательные поля email, имя, фамилия, номер телефона
    - Необязательные поля адрес, город
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

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'Users Profiles'


class BooksModel(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    author = models.ManyToManyField(to='AuthorModel')

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.title


class BooksSalesModel(models.Model):
    book = models.ForeignKey(to='BooksModel', on_delete=models.CASCADE, blank=True, null=True)
    sales = models.PositiveIntegerField(default=0, blank=True, null=True)
    sold_day = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Books sales'
        verbose_name_plural = 'Books sales'

    def __str__(self):
        return self.book.title


class AuthorModel(models.Model):
    author_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.author_name
