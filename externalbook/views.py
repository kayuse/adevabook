from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets, status
import json, requests
from rest_framework.response import Response
from .serializers.external_book_serializer import ExternalBookSerializer


# Create your views here.

class ExternalBookApiView(generics.ListAPIView):
    url = 'https://www.anapioficeandfire.com/api/books'
    serializer_class = ExternalBookSerializer

    def list(self, request):
        name = request.GET.get('name', '')

        url = self.url + "?name=" + name
        external_api_response = json.loads(requests.get(url).content)

        if len(external_api_response) <= 0:
            response_data = self.build_response(external_api_response, "success", status.HTTP_200_OK)
            return Response(response_data)

        serializer_data = ExternalBookSerializer(data=external_api_response, many=True)

        if serializer_data.is_valid(raise_exception=True):
            response_data = self.build_response(serializer_data.data, "success", status.HTTP_200_OK)
            return Response(response_data)

    @staticmethod
    def build_response(data, status, code, message=None):
        response = {"status_code": code,
                    "status": status,
                    "data": data}
        if message is not None:
            response['message'] = message
        return response
