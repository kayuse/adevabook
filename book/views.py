from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from .serializers.book_serializer import BookSerializer, Book


# Create your views here.


class BookApi(APIView):
    serializer_class = BookSerializer

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request):
        books = Book.objects
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        book_serializer = BookSerializer(data=request.data)

        if book_serializer.is_valid(raise_exception=True):
            validated_data = book_serializer.validated_data
            book_serializer.create(validated_data)
            return Response({'success': request.data})
