import io
from rest_framework import serializers
from ..models import Book, Author


class AuthorSerializer(serializers.BaseSerializer):
    # for reading
    def to_representation(self, obj):
        return obj.name

    # for writing
    def to_internal_value(self, obj):
        return obj


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ['name', 'isbn', 'country', 'number_of_pages', 'publisher', 'release_date', 'authors']

    def create(self, validated_data):
        authors = validated_data.pop('authors')
        book = Book.objects.create(**validated_data)
        authors_object = [Author(name=author, book=book) for author in authors]
        book.authors.set(authors_object, bulk=False)

        return validated_data
