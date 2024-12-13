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
        self.ta_user = TA.objects.create(user=self.ta_user, ta_dept='TADepartment')
        self.ta_user.save()

    @patch('django.contrib.messages.error')
    def test_edit_user_change_name(self, mock_message):
        post_data = {
            'id': self.ta_user.id,
            'old_role': 'TA',
            'role':'TA',
            'fname': 'Updated',
        }

        request = MagicMock()
        request.POST = post_data

        edit_user_account(request)

        user = User.objects.get(self.ta_user.id)

        # Assert that the user's details are updated
        user.refresh_from_db()
        self.assertEqual(user.fname, 'Updated')

        # Assert no errors in case of success
        mock_message.assert_not_called()

    @patch('django.contrib.messages.error')
    def test_edit_user_change_password(self, mock_message):
        post_data = {
            'id': self.ta_user.id,
            'old_role': 'TA',
            'role': 'TA',
            'password': 'password456',
        }

        request = MagicMock()
        request.POST = post_data

        edit_user_account(request)

        user = User.objects.get(self.ta_user.id)

        user.refresh_from_db()
        # Check password
        self.assertTrue(user.check_password('password456'))

        # Assert no errors in case of success
        mock_message.assert_not_called()

    @patch('django.contrib.messages.error')
    def test_edit_user_change_email(self, mock_message):
        post_data = {
            'id': self.ta_user.id,
            'old_role': 'TA',
            'role': 'TA',
            'email': 'newemail@example.com'
        }

        request = MagicMock()
        request.POST = post_data

        edit_user_account(request)

        # Assert that an error message is generated when attempting to change email
        mock_message.assert_called_with(request, "Cannot change email, create a new user instead")

    @patch('django.contrib.messages.error')
    def test_edit_user_change_role(self, mock_message):
        post_data = {
            'id': self.ta_user.id,
            'old_role': 'TA',
            'role': 'Supervisor',
            'password': 'password456',
        }

        request = MagicMock()
        request.POST = post_data

        edit_user_account(request)

        user = User.objects.get(self.ta_user.id)

        user.refresh_from_db()
        # Check password
        self.assertEqual(user.role, 'Supervisor')

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

        }

        request = MagicMock()
        request.POST = post_data

        delete_user_account(request)

        user = User.objects.get('ta@example.com')

        self.assertIsNotNone(user)

        # Assert no errors in case of success
        mock_message.assert_not_called()

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
        }

        request = MagicMock()
        request.POST = post_data

        delete_user_account(request)

        # Assert that an error message is generated when attempting to change email
        mock_message.assert_called_with(request, "User does not exist")

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from TAScheduler.models import Supervisor, TA, Instructor
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountManagementTests(TestCase):
    
    def setUp(self):
        # Create a superuser to login
        self.supervisor_user = User.objects.create_user(
            username='supervisor',
            password='password123',
        )
        supervisor_group = Group.objects.create(name='Supervisor')
        self.supervisor_user.groups.add(supervisor_group)
        
        # Create users for testing
        self.ta_user = User.objects.create_user(
            username='ta',
            password='password123',
        )
        ta_group = Group.objects.create(name='TA')
        self.ta_user.groups.add(ta_group)
        
        self.instructor_user = User.objects.create_user(
            username='instructor',
            password='password123',
        )
        instructor_group = Group.objects.create(name='Instructor')
        self.instructor_user.groups.add(instructor_group)
        
        # Create the Supervisor in the model
        Supervisor.objects.create(user=self.supervisor_user)
        TA.objects.create(user=self.ta_user)
        Instructor.objects.create(user=self.instructor_user)

        self.client.login(username='supervisor', password='password123')

    def test_account_management_page_renders(self):
        """Test that the account management page renders and displays the users"""
        response = self.client.get(reverse('account-management'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AccountManagement.html')
        self.assertContains(response, 'supervisor')
        self.assertContains(response, 'ta')
        self.assertContains(response, 'instructor')

    def test_create_user_account(self):
        """Test creating a user account via POST"""
        data = {
            'action': 'create',
            'username': 'newuser',
            'password': 'newpassword123',
            'role': 'TA'  # Or whatever role you're assigning
        }
        response = self.client.post(reverse('account-management'), data)
        new_user = User.objects.get(username='newuser')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_user.username, 'newuser')

    def test_edit_user_account(self):
        """Test editing a user account"""
        data = {
            'action': 'edit',
            'user_id': self.ta_user.id,
            'new_username': 'ta_updated',
        }
        response = self.client.post(reverse('account-management'), data)
        self.ta_user.refresh_from_db()  # Reload the user from the database
        self.assertEqual(self.ta_user.username, 'ta_updated')

    def test_delete_user_account(self):
        """Test deleting a user account"""
        data = {
            'action': 'delete',
            'user_id': self.ta_user.id,
        }
        response = self.client.post(reverse('account-management'), data)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.ta_user.id)

    def test_invalid_action(self):
        """Test invalid action post"""
        data = {
            'action': 'invalid_action',
        }
        response = self.client.post(reverse('account-management'), data)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Invalid action'})
