from django.contrib import admin

from .models import (ProfileModel, BooksModel)

admin.site.register(ProfileModel)
admin.site.register(BooksModel)

