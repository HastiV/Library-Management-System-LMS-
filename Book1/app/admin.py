from django.contrib import admin
from .models import Book, Author, Category

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'nationality']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'category', 'isbn', 'published_date', 'available_copies']
    search_fields = ['title', 'isbn']
    list_filter = ['category', 'author']


