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
        fields = ['id', 'name', 'isbn', 'country', 'number_of_pages', 'publisher', 'release_date', 'authors']

    def create(self, validated_data):
        authors = validated_data.pop('authors')
        book = Book.objects.create(**validated_data)
        authors_object = [Author(name=author) for author in authors]
        book.authors.set(authors_object, bulk=False)
        return BookSerializer(book)

    def update(self, instance, validated_data):
        authors = validated_data.pop('authors')

        instance.name = validated_data.get('name')
        instance.isbn = validated_data.get('isbn')
        instance.country = validated_data.get('country')
        instance.number_of_pages = validated_data.get('number_of_pages')
        instance.publisher = validated_data.get('publisher')
        instance.release_date = validated_data.get('release_date')

        authors_object = [Author(name=author) for author in authors]
        instance.authors.all().delete()
        instance.authors.set(authors_object, bulk=False)

        instance.save()

        return BookSerializer(instance)
