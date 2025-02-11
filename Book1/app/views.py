from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Book, Author, Category
from .serializers import BookSerializer, AuthorSerializer, CategorySerializer, BookReservationSerializer

# List all books
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Get details of a single book
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# List all authors
class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

# List all categories
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# book search api
class CustomPagination(PageNumberPagination):
    page_size = 5  # Default page size
    page_size_query_param = 'page_size'
    max_page_size = 50

class BookSearchView(ListAPIView):
    serializer_class = BookSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        query = self.request.query_params.get('query', '').strip()
        if not query:
            return Book.objects.none()  # Return empty if no query provided

        search_terms = query.split()  # Split multi-word searches
        q_objects = Q()

        for term in search_terms:
            q_objects |= Q(title__icontains=term) | Q(author__name__icontains=term)

        return Book.objects.filter(q_objects).distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        if not queryset.exists():
            return Response(
                {"message": "No books found.", "results": []},
                status=status.HTTP_200_OK
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    

# book copies
class BookReserveView(APIView):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)

        if book.available_copies > 0:
            serializer = BookReservationSerializer(book, data={}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Book reserved successfully!", "book": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No copies available for reservation."}, status=status.HTTP_400_BAD_REQUEST)
