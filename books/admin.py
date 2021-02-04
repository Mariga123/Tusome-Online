from django.contrib import admin
from .models import Author, Book, Identifier, ImageLinks
# Register your models here.


class AuthorInline(admin.StackedInline):
    model = Author


class BookAdmin(admin.ModelAdmin):
    list_display = ['title',]
    #inlines = [AuthorInline]


admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Identifier)
admin.site.register(ImageLinks)