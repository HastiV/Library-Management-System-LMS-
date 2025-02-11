from django.urls import path
from .views import BookListView, BookDetailView, AuthorListView, CategoryListView, BookSearchView, BookReserveView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('api/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('books/search/', BookSearchView.as_view(), name='book-search'),
    path('books/<int:pk>/reserve/', BookReserveView.as_view(), name='book-reserve'),        
]
