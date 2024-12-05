from django.test import TestCase
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
