from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.auth.models import Group

User = get_user_model()

class AccountManagementCreateTests(TestCase):

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

        self.ta_user = User.objects.create_user(
            email='ta@example.com',
            password='tapassword123',
            fname='TA',
            lname='User',
            address='456 TA Road',
            phone_number='0987654321'
        )

        self.ta_user.save()


    def test_supervisor_create_user_success(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/account-management/")
        self.assertEqual(response.status_code, 200)

        data = {
            'email': 'newuser@example.com',
            'fname': 'New',
            'lname': 'User',
            'address': '789 New Road',
            'phone_number': '1122334455',
            'password': 'newuserpassword123',
            'action' : 'create'
        }
        response = self.client.post("/account-management/", data)
        self.assertEqual(response.status_code, 302) #status is a type 3XX cause our view redirects back to itself

        new_user = User.objects.get(email='newuser@example.com')
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.email, 'newuser@example.com')

    def test_supervisor_create_user_incomplete_form(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/account-management/")
        self.assertEqual(response.status_code, 200)

        data = {
            'fname': 'Incomplete',
            'lname': 'Form',
            'address': 'Missing Email Road',
            'phone_number': '0000000000',
            'password': 'incompletepassword123',
            'action':'create'
        }
        response = self.client.post("/account-management/", data)
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request)) #Retrieve all logged messages in the current request session

        self.assertTrue(
            any("Email cannot be empty" in str(message) for message in messages),
            "Expected message about missing email not found in the session messages.") #Check if an error about no email input is in it

    #If someone creates an account with an email and password but no other fields, it should work and set empty fields to null/blank string
    def test_supervisor_create_user_empty_form(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/account-management/")
        self.assertEqual(response.status_code, 200)

        data = {
            'email': 'newuser@example.com',
            'password': 'newuserpassword123',
            'action': 'create'
        }
        response = self.client.post("/account-management/", data)
        self.assertEqual(response.status_code, 302)

        new_user = User.objects.get(email='newuser@example.com')
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.email, 'newuser@example.com')

    def test_supervisor_create_user_non_unique_email(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/account-management/")
        self.assertEqual(response.status_code, 200)

        data = {
            'email': 'supervisor@example.com',
            'fname': 'Duplicate',
            'lname': 'User',
            'address': '789 Duplicate Lane',
            'phone_number': '1122336677',
            'password': 'duplicatepassword123',
            'action' : 'create'   #action field is used in our view to specify the kind of post(creating, editing, deleting).
        }

        response = self.client.post("/account-management/", data)
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any("Email already exists in the system" in str(message) for message in messages),
            "Expected message about email already being in the system.") #Model now returns a message indicating the email sent wasn't unique
        
    def test_ta_access_account_management(self):
        self.client.login(email='ta@example.com', password='tapassword123')

        response = self.client.get("/account-management/")

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html') #FIX := Our page renders a 403 instead of redirecting back to the home page or "/", which in our case is the login 

        # self.assertRedirects(response, "/")  

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
        self.assertTemplateUsed(response, '403.html') #FIX := Our page renders a 403 instead of redirecting back to the home page or "/", which in our case is the login 

        # self.assertRedirects(response, "/")  