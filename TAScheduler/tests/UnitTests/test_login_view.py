from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Group
from TAScheduler.models import Supervisor

User = get_user_model()

class LoginViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
        )

        self.login_url = "/"
        self.account_management_url = "AccountManagement/"

    def test_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_valid_user(self):
        response = self.client.post(self.login_url, {
            'username': self.user.email,
            'password': 'password123',
        })

        self.assertRedirects(response, self.account_management_url)

        user = authenticate(username=self.user.email, password='password123')
        self.assertTrue(user is not None)
        self.assertEqual(user.username, self.user.email)

    def test_login_invalid_user(self):
        response = self.client.post(self.login_url, {
            'username': self.user.email,
            'password': 'wrongpassword',
        })

        self.assertFormError(response, 'form', 'password', 'Your username and password didn’t match. Please try again.')

    def test_redirect_authenticated_user(self):
        self.client.login(username=self.user.email, password='password123')
        response = self.client.get(self.login_url, follow=True)

        self.assertRedirects(response, self.account_management_url)