from django.contrib import admin

from .models import (ProfileModel, BooksModel, BooksSalesModel)


class BooksSalesInline(admin.StackedInline):
    model = BooksSalesModel


class BooksAdmin(admin.ModelAdmin):
    inlines = (BooksSalesInline,)
    model = BooksModel


admin.site.register(ProfileModel)
admin.site.register(BooksModel, BooksAdmin)
admin.site.register(BooksSalesModel)
