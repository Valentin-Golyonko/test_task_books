from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.db import models

UserModel = get_user_model()


class Profile(models.Model):
    """
    - Обязательные поля email, имя, фамилия, номер телефона
    - Необязательные поля адрес, город
    """
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30, unique=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'Users Profiles'


class AuthorModel(models.Model):
    author_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.author_name


class BooksModel(models.Model):
    book_title = models.CharField(max_length=200)
    book_isbn = models.CharField(max_length=20)
    book_author = models.ManyToManyField(AuthorModel)

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['id']

    def __str__(self):
        return self.book_title


class BooksSalesModel(models.Model):
    book = models.ForeignKey(BooksModel, on_delete=models.CASCADE, blank=True, null=True)
    sales = models.PositiveIntegerField(default=0, blank=True, null=True)
    sold_day = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Books sales'
        verbose_name_plural = 'Books sales'

    def __str__(self):
        return self.book.book_title


class Notification(models.Model):
    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    message = models.CharField(max_length=50, blank=True, null=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-id']

    def __str__(self):
        return self.message
