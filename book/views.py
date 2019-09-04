from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import Http404
from .serializers.book_serializer import BookSerializer, Book


# Create your views here.


class BookApi(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def retrieve(self, request, pk, *args, **kwargs):
        books = Book.objects
        book = books.filter(id=pk).first()
        if book is None:
            return Response(self.build_response([], 'Not found', status.HTTP_404_NOT_FOUND),
                            status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book)
        return Response(self.build_response(serializer.data, 'success', status.HTTP_200_OK))

    def list(self, request, *args, **kwargs):
        books = Book.objects
        serializer = BookSerializer(books, many=True)

        return Response(self.build_response(serializer.data, 'success', status.HTTP_200_OK))

    def create(self, request, *args, **kwargs):
        book_serializer = BookSerializer(data=request.data)

        if book_serializer.is_valid(raise_exception=True):
            validated_data = book_serializer.validated_data
            result = book_serializer.create(validated_data)
            data = {"book": result.data}
            return Response(self.build_response(data, 'success', status.HTTP_201_CREATED))

    def patch(self, request, pk):
        return Response({'success': request.data})

    def update(self, request, pk, *args, **kwargs):
        # print(Book.objects.all()[0].authors.name)

        serializer = BookSerializer(Book.objects, data=request.data)
        if serializer.is_valid(raise_exception=True):
            book_update = serializer.update(Book.objects.get(id=pk), serializer.validated_data)
            data = {"book": book_update.data}
            return Response(self.build_response(data, 'success', status.HTTP_201_CREATED))

    def destroy(self, request, pk, *args, **kwargs):
        books = Book.objects
        book = books.filter(id=pk).first()
        if book is None:
            return Response(self.build_response([], 'Not found', status.HTTP_404_NOT_FOUND),
                            status=status.HTTP_404_NOT_FOUND)
        
        book.delete()
        return Response(self.build_response([], 'success', status.HTTP_204_NO_CONTENT,
                                            "The book My First Book was deleted successfully"))

    @staticmethod
    def build_response(data, status, code, message=None):
        response = {"status_code": code,
                    "status": status,
                    "data": data}
        if message is not None:
            response['message'] = message
        return response
