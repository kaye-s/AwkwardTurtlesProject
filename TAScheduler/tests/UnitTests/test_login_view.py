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
        Supervisor.objects.create(user=self.user, admin_dept="Computer Science") #Fix for test_redirect_authenticated_user

        self.login_url = "/"
        self.account_management_url = "/account-management/"

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
        self.assertEqual(user.email, self.user.email) #FIX := model doesn't have a username field so it returned none for user.username

    def test_login_invalid_user(self):
        response = self.client.post(self.login_url, {
            'username': self.user.email,
            'password': 'wrongpassword',
        })
        self.assertContains(response, "Please enter a correct email and password. Note that both fields may be case-sensitive.", html=True) #FIX := response renders static html and not dynmaic with forms
        # self.assertFormError(response, 'form', 'password', 'Your username and password didn’t match. Please try again.')

    def test_redirect_authenticated_user(self):
        self.client.login(username=self.user.email, password='password123') #FIX := user needs to be a supervisor
        response = self.client.get(self.login_url, follow=True)

        self.assertRedirects(response, self.account_management_url)