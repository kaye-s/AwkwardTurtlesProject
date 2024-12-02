from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.auth.models import Group
from TAScheduler.models import TA, Instructor

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

        #Ta to test editing
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

    def test_supervisor_edit_nothing(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/account-management/")
        self.assertEqual(response.status_code, 200)

        data = {
            'action' : 'edit'
        }
        response = self.client.post("/account-management/", data)
        self.assertEqual(response.status_code, 302) #status is a type 3XX cause our view redirects back to itself

    def test_supervisor_edit_user_fname(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/account-management/")
        self.assertEqual(response.status_code, 200)
        #taEmail = self.ta_user.email
        #id = TA.objects.get(email = taEmail)
        #cur_user = id.user_id
        data = {
            'email': 'ta@example.com',
            'fname': 'John',
            'action' : 'edit'
        }
        response = self.client.post("/account-management/", data)
        self.assertEqual(response.status_code, 302) #status is a type 3XX cause our view redirects back to itself

        self.assertEqual('John', self.ta_user.fname)

    def test_supervisor_edit_user_role(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/account-management/")
        self.assertEqual(response.status_code, 200)

        data = {
            'email': 'ta@example.com',
            'role': 'Instructor',
            'action' : 'edit'
        }
        response = self.client.post("/account-management/", data)
        self.assertEqual(response.status_code, 302) #status is a type 3XX cause our view redirects back to itself

        self.assertEqual('Instructor', self.ta_user.role)

    def test_supervisor_edit_user_pass(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/account-management/")
        self.assertEqual(response.status_code, 200)

        data = {
            'email': 'ta@example.com',
            'password': 'tapassword456',
            'action' : 'edit'
        }
        response = self.client.post("/account-management/", data)
        self.assertEqual(response.status_code, 302) #status is a type 3XX cause our view redirects back to itself

        self.assertEqual('tapassword456', self.ta_user.password)

    def test_supervisor_edit_user_email(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/account-management/")
        self.assertEqual(response.status_code, 200)

        data = {
            'email': 'email@example.com',
            'action' : 'edit'
        }
        response = self.client.post("/account-management/", data)
        self.assertEqual(response.status_code, 302) #status is a type 3XX cause our view redirects back to itself

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any("Cannot edit email, please instead create a new account for the user" in str(message) for message in messages),
            "Expected a message - inability to edit email")

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


