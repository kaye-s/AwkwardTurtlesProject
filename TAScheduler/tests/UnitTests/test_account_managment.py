from django.test import TestCase
from unittest.mock import MagicMock, patch
from django.contrib.auth.models import User
from django.contrib import messages
from TAScheduler.models import Supervisor, TA, Instructor
from TAScheduler.utils.account_management import create_user_account, edit_user_account, delete_user_account
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountManagementCreateTests(TestCase):

    def setUp(self):
        self.url = reverse('account-management')

    @patch('django.contrib.messages.error')
    def test_create_user_success(self, mock_message):
        post_data = {
            'email': 'newuser@example.com',
            'fname': 'John',
            'lname': 'Doe',
            'role': 'TA',
            'dept': 'Computer Science',
            'phone_number': '1234567890',
            'address1': '123 Main St',
            'address2': 'Some City',
            'password': 'password123',
        }

        request = MagicMock()
        request.POST = post_data

        create_user_account(request)

        user = User.objects.get(email='newuser@example.com')

        # Assert user is created
        self.assertEqual(user.fname, 'John')
        self.assertEqual(user.lname, 'Doe')

        # Assert role is created
        ta_obj = TA.objects.get(user=user)
        self.assertEqual(ta_obj.ta_dept, 'Computer Science')

        # Assert no errors in case of success
        mock_message.assert_not_called()

    @patch('django.contrib.messages.error')
    def test_create_user_invalid_email_empty(self, mock_message):
        post_data = {
            'email': 'None',  # Invalid email
            'fname': 'John',
            'lname': 'Doe',
            'role': 'TA',
            'dept': 'Computer Science',
            'phone_number': '1234567890',
            'address1': '123 Main St',
            'address2': 'Some City',
            'password': 'password123',
        }

        request = MagicMock()
        request.POST = post_data

        create_user_account(request)

        mock_message.assert_called_with(request, "Email cannot be empty")

    @patch('django.contrib.messages.error')
    def test_create_user_email_exists(self, mock_message):
        test_user = User.objects.create_user(
            email='existinguser@example.com',
            password='password123',
            fname='Existing',
            lname='User',
            phone_number='9876543210',
            address='123 Main St'
        )
        test_user.save()

        post_data = {
            'email': 'existinguser@example.com',  # Email already exists
            'fname': 'John',
            'lname': 'Doe',
            'role': 'TA',
            'dept': 'Computer Science',
            'phone_number': '1234567890',
            'address1': '123 Main St',
            'address2': 'Some City',
            'password': 'password123',
        }

        request = MagicMock()
        request.POST = post_data

        create_user_account(request)

        # Assert that an error message is generated for existing email
        mock_message.assert_called_with(request, "Email already exists in the system")

    @patch('django.contrib.messages.error')
    def test_create_user_no_password(self, mock_message):
        post_data = {
            'email': 'newuser@example.com',
            'fname': 'John',
            'lname': 'Doe',
            'role': 'TA',
            'dept': 'Computer Science',
            'phone_number': '1234567890',
            'address1': '123 Main St',
            'address2': 'Some City',
        }

        request = MagicMock()
        request.POST = post_data

        create_user_account(request)

        # Assert that an error message is generated for no password
        mock_message.assert_called_with(request, "Must create a password")

    @patch('django.contrib.messages.error')
    def test_create_user_email_password_only(self, mock_message):
        post_data = {
            'email': 'newuser@example.com',
            'password': 'password123',
        }

        request = MagicMock()
        request.POST = post_data

        create_user_account(request)

        user = User.objects.get(email='newuser@example.com')

        #Check password
        self.assertTrue(user.check_password('password123'))
        # Assert other fields are empty
        self.assertEqual(user.fname, 'None')
        self.assertEqual(user.lname, 'None')

        # Assert no errors in case of success
        mock_message.assert_not_called()


