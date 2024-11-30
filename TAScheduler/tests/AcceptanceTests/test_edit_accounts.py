from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.auth.models import Group

User = get_user_model()

#CANNOT RUN THESE TESTS UNTIL I FIGURE OUT WHAT THE PATH IS FOR THE EDIT ACCOUNTS FORM
class AccountManagementTests(TestCase):

    def setUp(self):
        self.supervisor_user = User.objects.create_user(
            email='supervisor@example.com',
            password='superpassword123',
            fname='Supervisor',
            lname='User',
            address='123 Supervisor Lane',
            phone_number='1234567890'
        )

        supervisor_group, _ = Group.objects.get_or_create(name='Supervisor')
        self.supervisor_user.groups.add(supervisor_group)
        self.supervisor_user.save()

        self.test_user = User.objects.create_user(
            email='user@example.com',
            password='userpassword123',
            fname='User',
            lname='Example',
            address='123 Example Lane',
            phone_number='9876543210'
        )

    def test_supervisor_edit_user_success(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        data = {
            'user_id': self.test_user.id,
            'fname': 'Updated',
            'lname': 'User'
        }

        response = self.client.post("AccountManagement/", data)

        updated_user = User.objects.get(id=self.test_user.id)
        self.assertEqual(updated_user.fname, 'Updated')
        self.assertEqual(updated_user.lname, 'User')

        self.assertContains(response, "User user@example.com has been updated.")

        self.assertRedirects(response, "AccountManagement/")

    def test_supervisor_edit_user_incomplete_form(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        data = {
            'user_id': self.test_user.id,
            'lname': 'Updated'
        }
        response = self.client.post("AccountManagement/", data)

        self.assertFormError(response, 'form', 'fname', 'This field is required.')

        unchanged_user = User.objects.get(id=self.test_user.id)
        self.assertEqual(unchanged_user.fname, 'User')

    def test_supervisor_edit_user_non_unique_email(self):
        self.new_user = User.objects.create_user(
            email='newuser@example.com',
            password='newuserpassword123',
            fname='New',
            lname='User',
            address='789 New Road',
            phone_number='1122334455'
        )

        self.client.login(email='supervisor@example.com', password='superpassword123')

        data = {
            'user_id': self.test_user.id,
            'email': 'newuser@example.com',
            'fname': 'Duplicate',
            'lname': 'User'
        }
        response = self.client.post("AccountManagement/", data)

        self.assertContains(response, 'A user with that email address already exists.')

        unchanged_user = User.objects.get(id=self.test_user.id)
        self.assertEqual(unchanged_user.email, 'user@example.com')

    def test_ta_edit_user_access_denied(self):
        self.client.login(email='ta@example.com', password='tapassword123')

        data = {
            'user_id': self.test_user.id,
            'fname': 'Unauthorized',
            'lname': 'Edit'
        }

        response = self.client.post("AccountManagement/", data)

        self.assertRedirects(response, "/")
