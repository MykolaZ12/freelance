from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class UserTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_superuser(email="example@mail.com", password="pass")
        self.token = AccessToken.for_user(self.user)
        self.payload = {
            'email': 'example@gmail.com',
            'password': 'admin123456',
            'first_name': "Mykola",
            'last_name': "Riabchenko",
            'phone_number': "+380684567569",
        }

    def test_valid_customer_register(self):
        role = "Customer"
        self.payload['user_type'] = role
        response = self.client.post('/api/auth/users/', self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(email=self.payload['email']).user_type, role)

    def test_valid_executor_register(self):
        role = "Executor"
        self.payload['user_type'] = role
        response = self.client.post('/api/auth/users/', self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(email=self.payload['email']).user_type, role)

    def test_invalid_user_register(self):
        role = "596"
        self.payload['user_type'] = role
        response = self.client.post('/api/auth/users/', self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_users(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get('/api/auth/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(f'/api/auth/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
