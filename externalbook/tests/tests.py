from rest_framework.test import APITestCase
import json
from django.urls import reverse
from rest_framework import status


class ExternalBookTestCase(APITestCase):
    url = reverse('external-books-list')

    def test_can_get_books(self):
        response = self.client.get(self.url, format='json')
        new_book_dict = json.loads(response.content)
        cleaned_data = new_book_dict['data']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(cleaned_data), 0)
