from rest_framework import serializers
from .models import Book, Author, Identifier, ImageLinks


class ImageLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageLinks
        exclude = ['id']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        exclude = ['id']


class IdentifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Identifier
        exclude = ['id']


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    industryIdentifiers = IdentifierSerializer(Identifier, many=True)
    imageLinks = ImageLinksSerializer(ImageLinks)

    class Meta:
        model = Book
        exclude = ['id']

