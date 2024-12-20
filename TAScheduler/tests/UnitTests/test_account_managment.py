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


class AccountManagementEditTests(TestCase):

    def setUp(self):
        self.ta_user = User.objects.create_user(
            email='ta@example.com',
            password='tapassword123',
            fname='TA',
            lname='User',
            phone_number='9876543210',
            address='456 TA Lane'
        )
        self.ta_user.save()
        self.ta_user = TA(user=self.ta_user, ta_dept="dept")
        self.ta_user.save()

    @patch('django.contrib.messages.error')
    def test_edit_user_change_name(self, mock_message):
        user = self.ta_user.user
        post_data = {
            'user_id': user.email,
            'old_role': 'TA',
            'role': 'TA',
            'fname': 'Updated',
        }

        request = MagicMock()
        request.POST = post_data

        edit_user_account(request)

        user = User.objects.get(id=self.ta_user.id)

        # Assert that the user's details are updated
        user.refresh_from_db()
        self.assertEqual(user.fname, 'Updated')

        # Assert no errors in case of success
        mock_message.assert_not_called()

    @patch('django.contrib.messages.error')
    def test_edit_user_change_password(self, mock_message):
        user = self.ta_user.user
        post_data = {
            'user_id': user.email,
            'old_role': 'TA',
            'role': 'TA',
            'password': 'password456',
        }

        request = MagicMock()
        request.POST = post_data

        edit_user_account(request)

        user = User.objects.get(id=self.ta_user.id)

        user.refresh_from_db()
        # Check password
        self.assertTrue(user.check_password('password456'))

        # Assert no errors in case of success
        mock_message.assert_not_called()

    @patch('django.contrib.messages.error')
    def test_edit_user_change_email(self, mock_message):
        user = self.ta_user.user
        post_data = {
            'user_id': user.email,
            'old_role': 'TA',
            'role': 'TA',
            'email': 'newemail@example.com',
            'action': 'edit',
        }

        request = MagicMock()
        request.POST = post_data

        edit_user_account(request)

        # Assert that an error message is generated when attempting to change email
        mock_message.assert_called_with(request, "Cannot change email, create a new user instead")

    @patch('django.contrib.messages.error')
    def test_edit_user_change_role(self, mock_message):
        user = self.ta_user.user
        post_data = {
            'user_id': user.email,
            'old_role': 'TA',
            'role': 'Supervisor',
            'password': 'password456',
        }

        request = MagicMock()
        request.POST = post_data

        edit_user_account(request)

        user = User.objects.get(id=self.ta_user.id)

        user.refresh_from_db()
        # Check password
        checks = Supervisor.objects.filter(user=user).exists()
        self.assertTrue(checks)

        # Assert no errors in case of success
        mock_message.assert_not_called()

class AccountManagementDeleteTests(TestCase):

    def setUp(self):
        self.ta_user = User.objects.create_user(
            email='ta@example.com',
            password='tapassword123',
            fname='TA',
            lname='User',
            phone_number='9876543210',
            address='456 TA Lane'
        )
        self.ta_user = TA.objects.create(user=self.ta_user, ta_dept='TADepartment')
        self.ta_user.save()

    @patch('django.contrib.messages.error')
    def test_delete_nothing(self, mock_message):
        post_data = {
            'action': 'delete',
        }

        request = MagicMock()
        request.POST = post_data

        delete_user_account(request)

        user = User.objects.filter(email='ta@example.com')

        self.assertIsNotNone(user)

        # Assert no errors in case of success
        mock_message.assert_called()

    @patch('django.contrib.messages.error')
    def test_delete_user_success(self, mock_message):
        useremail = self.ta_user.user
        useremail = useremail.email
        post_data = {
            'email': useremail,
        }

        request = MagicMock()
        request.POST = post_data

        delete_user_account(request)

        user = User.objects.filter(email='ta@example.com').exists()

        self.assertFalse(user)

        # Assert no errors in case of success
        mock_message.assert_not_called()

    @patch('django.contrib.messages.error')
    def test_delete_user_does_not_exist(self, mock_message):
        post_data = {
            'id': 'email@example.com',
            'action': 'delete',
        }

        request = MagicMock()
        request.POST = post_data

        delete_user_account(request)

        # Assert that an error message is generated when attempting to change email
        mock_message.assert_called_with(request, "User does not exist")
