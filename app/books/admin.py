from django.contrib import admin

from .models import (Profile, BooksModel, BooksSalesModel,
                     AuthorModel, Notification)


class BooksSalesInline(admin.StackedInline):
    model = BooksSalesModel


class BooksAdmin(admin.ModelAdmin):
    inlines = (BooksSalesInline,)
    model = BooksModel


class AuthorAdmin(admin.ModelAdmin):
    model = AuthorModel


admin.site.register(Profile)
admin.site.register(BooksModel, BooksAdmin)
admin.site.register(BooksSalesModel)
admin.site.register(Notification)
admin.site.register(AuthorModel, AuthorAdmin)
