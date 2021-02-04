from rest_framework import filters, viewsets
from .models import Book
from .serializers import BookSerializer
import django_filters.rest_framework


class BooksView(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    allowed_methods = ['GET']
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter]
    filter_fields = ['title', 'authors', 'language', 'publishedDate']
    search_fields = ['title', 'authors__name', 'language', 'publishedDate']

