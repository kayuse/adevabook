from django.test import TestCase
from rest_framework.test import APITestCase
import json
from django.urls import reverse
from rest_framework import status


def create_rest_data():
    data = {
        "name": "Bankai",
        "isbn": "123-32132435679",
        "authors": ["sdsd", "sssdd"],
        "country": "Nigeria",
        "number_of_pages": 300,
        "publisher": "Adeva Books Ministry",
        "release_date": "2019-12-01"
    }
    return data


# Create your tests here.

class BookTestCase(APITestCase):
    url = reverse('book-list')

    def create_data(self):
        return self.client.post(self.url, create_rest_data(), format='json')

    def test_can_create_book(self):
        response = self.create_data()
        new_book_dict = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cleaned_data = new_book_dict['data']['book']
        cleaned_data.pop('id')

        self.assertEqual(cleaned_data, create_rest_data())

    def test_can_get_book(self):
        data = json.loads(self.create_data().content)

        id = str(data['data']['book']['id'])
        response = self.client.get(self.url + "/" + id, format='json')

        new_book_dict = json.loads(response.content)
        cleaned_data = new_book_dict['data']
        cleaned_data.pop('id')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(cleaned_data, create_rest_data())

    def test_can_get_books(self):
        self.create_data()

        response = self.client.get(self.url, format='json')
        new_book_dict = json.loads(response.content)
        cleaned_data = new_book_dict['data']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(cleaned_data), 0)

    def test_can_update_book(self):
        data = json.loads(self.create_data().content)
        updated_rest_data = create_rest_data()
        updated_rest_data['name'] = 'Adeva Community'
        id = str(data['data']['book']['id'])
        response = self.client.patch(self.url + "/" + id, updated_rest_data, format='json')

        new_book_dict = json.loads(response.content)
        cleaned_data = new_book_dict['data']['book']
        cleaned_data.pop('id')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(cleaned_data, updated_rest_data)

    def test_can_delete_book(self):
        data = json.loads(self.create_data().content)

        id = str(data['data']['book']['id'])
        response = self.client.delete(self.url + "/" + id, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
