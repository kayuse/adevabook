import io
from rest_framework import serializers
from datetime import date


class AuthorSerializer(serializers.BaseSerializer):
    # for reading
    def to_representation(self, obj):
        return obj

    # for writing
    def to_internal_value(self, obj):
        return obj


class ExternalBookSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=1050)
    isbn = serializers.CharField(max_length=20)
    country = serializers.CharField(max_length=1000)
    numberOfPages = serializers.IntegerField()
    publisher = serializers.CharField(max_length=2000)
    released = serializers.DateTimeField()
    authors = AuthorSerializer(many=True)

    def to_representation(self, obj):

        return {
            "name": obj['name'],
            "isbn": obj['isbn'],
            "country": obj['country'],
            "number_of_pages": obj['numberOfPages'],
            "publisher": obj['publisher'],
            "release_date": obj['released'].date(),
            "authors": obj['authors']
        }
