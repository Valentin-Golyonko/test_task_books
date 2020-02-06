from django.contrib import admin

from .models import (Profile, BooksModel, BookSales,
                     AuthorModel, Notification)


class BooksSalesInline(admin.StackedInline):
    model = BookSales


class BooksAdmin(admin.ModelAdmin):
    inlines = (BooksSalesInline,)
    model = BooksModel


class AuthorAdmin(admin.ModelAdmin):
    model = AuthorModel


admin.site.register(Profile)
admin.site.register(BooksModel, BooksAdmin)
admin.site.register(BookSales)
admin.site.register(Notification)
admin.site.register(AuthorModel, AuthorAdmin)
