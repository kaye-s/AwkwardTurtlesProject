from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.auth.models import Group

User = get_user_model()

class AccountManagementEditTests(TestCase):

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

        #Ta to test deletion
        self.ta_user = User.objects.create_user(
            email='ta@example.com',
            password='tapassword123',
            fname='TA',
            lname='User',
            address='456 TA Road',
            phone_number='0987654321'
        )

        ta_group, _ = Group.objects.get_or_create(name='TA')
        self.ta_user.groups.add(ta_group)
        self.ta_user.save()

        # Supervisor to test deletion
        self.ta_user = User.objects.create_user(
            email='supervisor2@example.com',
            password='super2password123',
            fname='Super2',
            lname='User',
            address='456 Supervisor Road',
            phone_number='0987654321'
        )

    def test_supervisor_delete_nothing(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/account-management/")
        self.assertEqual(response.status_code, 200)

        data = {
            'action' : 'delete'
        }
        response = self.client.post("/account-management/", data)
        self.assertEqual(response.status_code, 302) #status is a type 3XX cause our view redirects back to itself

    def test_supervisor_delete_user_success(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/account-management/")
        self.assertEqual(response.status_code, 200)

        data = {
            'email': 'ta@example.com',
            'action': 'delete'
        }
        response = self.client.post("/account-management/", data)
        self.assertEqual(response.status_code, 302)  # status is a type 3XX cause our view redirects back to itself

        new_user = User.objects.get(email='ta@example.com')
        self.assertIsNone(new_user)

    def test_supervisor_delete_super(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/account-management/")
        self.assertEqual(response.status_code, 200)

        data = {
            'email': 'super2@example.com',
            'action': 'delete'
        }
        response = self.client.post("/account-management/", data)
        self.assertEqual(response.status_code, 302)  # status is a type 3XX cause our view redirects back to itself

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any("Cannot delete supervisor" in str(message) for message in
                messages),
            "Expected a message - cannot delete supervisor")

    def test_ta_access_account_management(self):
        self.client.login(email='ta@example.com', password='tapassword123')

        response = self.client.get("/account-management/")

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response,
                                '403.html')


    def test_instructor_access_account_management(self):
        User.objects.create_user(
            email='instructor@example.com',
            password='instructorpassword123',
            fname='Instructor',
            lname='User',
            address='789 Instructor Lane',
            phone_number='1239874560'
        )

        self.client.login(email='instructor@example.com', password='instructorpassword123')

        response = self.client.get("/account-management/")

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response,
                                '403.html')