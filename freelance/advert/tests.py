import io
from unittest.mock import Mock
from django.core.files import File
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from freelance.advert.models import AdvertFile

User = get_user_model()


class AdvertTest(APITestCase):
    def setUp(self) -> None:
        self.customer = User.objects.create_user(email="example@mail.com", password="pass",
                                                 first_name="first_name", last_name="last_name",
                                                 user_type="Customer")
        self.executor = User.objects.create_user(email="example2@mail.com", password="pass",
                                                 first_name="first_name",
                                                 last_name="last_name",
                                                 user_type="Executor")
        self.payload = {
            'title': 'example@gmail.com',
            'description': 'admin123456',
            'award': 100,
            'status': "WAI",
        }

    def test_valid_create_advert(self):
        url = "/api/advert/"
        token = AccessToken.for_user(self.customer)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_create_advert(self):
        url = "/api/advert/"
        token = AccessToken.for_user(self.executor)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_advert_with_files(self):
        url = "/api/advert/"
        mock_file = Mock(spec=File)
        file_list = [mock_file, mock_file, mock_file]

        token = AccessToken.for_user(self.customer)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(url, {**self.payload, "files": file_list}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(AdvertFile.objects.all()), 3)

