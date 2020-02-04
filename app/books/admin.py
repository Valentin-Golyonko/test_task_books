from django.contrib import admin

from .models import (ProfileModel, BooksModel, BooksSalesModel,
                     AuthorModel, NotificationsModel)


class BooksSalesInline(admin.StackedInline):
    model = BooksSalesModel


class BooksAdmin(admin.ModelAdmin):
    inlines = (BooksSalesInline,)
    model = BooksModel


class AuthorAdmin(admin.ModelAdmin):
    model = AuthorModel


admin.site.register(ProfileModel)
admin.site.register(BooksModel, BooksAdmin)
admin.site.register(BooksSalesModel)
admin.site.register(NotificationsModel)
admin.site.register(AuthorModel, AuthorAdmin)
