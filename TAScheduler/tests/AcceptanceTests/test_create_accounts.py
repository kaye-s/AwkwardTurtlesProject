# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Group

# User = get_user_model()

# class AccountManagementTests(TestCase):

#     def setUp(self):
#         self.supervisor_user = User.objects.create_user(
#             email='supervisor@example.com',
#             password='superpassword123',
#             fname='Supervisor',
#             lname='User',
#             address='123 Supervisor Lane',
#             phone_number='1234567890'
#         )

#         supervisor_group, _ = Group.objects.get_or_create(name='Supervisor')
#         self.supervisor_user.groups.add(supervisor_group)
#         self.supervisor_user.save()

#         self.ta_user = User.objects.create_user(
#             email='ta@example.com',
#             password='tapassword123',
#             fname='TA',
#             lname='User',
#             address='456 TA Road',
#             phone_number='0987654321'
#         )


#     def test_supervisor_create_user_success(self):
#         self.client.login(email='supervisor@example.com', password='superpassword123')

#         response = self.client.get("AccountManagement/")
#         self.assertEqual(response.status_code, 200)

#         data = {
#             'email': 'newuser@example.com',
#             'fname': 'New',
#             'lname': 'User',
#             'address': '789 New Road',
#             'phone_number': '1122334455',
#             'password': 'newuserpassword123',
#         }
#         response = self.client.post("AccountManagement/", data)
#         self.assertEqual(response.status_code, 200)

#         new_user = User.objects.get(email='newuser@example.com')
#         self.assertIsNotNone(new_user)
#         self.assertEqual(new_user.email, 'newuser@example.com')

#     def test_supervisor_create_user_incomplete_form(self):
#         self.client.login(email='supervisor@example.com', password='superpassword123')

#         response = self.client.get("AccountManagement/")
#         self.assertEqual(response.status_code, 200)

#         data = {
#             'fname': 'Incomplete',
#             'lname': 'Form',
#             'address': 'Missing Email Road',
#             'phone_number': '0000000000',
#             'password': 'incompletepassword123',
#         }
#         response = self.client.post("AccountManagement/", data)

#         self.assertFormError(response, 'form', 'email', 'This field is required.')

#     def test_supervisor_create_user_non_unique_email(self):
#         self.client.login(email='supervisor@example.com', password='superpassword123')

#         response = self.client.get("AccountManagement/")
#         self.assertEqual(response.status_code, 200)
#         data = {
#             'email': 'supervisor@example.com',
#             'fname': 'Duplicate',
#             'lname': 'User',
#             'address': '789 Duplicate Lane',
#             'phone_number': '1122336677',
#             'password': 'duplicatepassword123',
#         }
#         response = self.client.post("AccountManagement/", data)

#         self.assertContains(response, 'A user with that email address already exists.')

#     def test_ta_access_account_management(self):
#         self.client.login(email='ta@example.com', password='tapassword123')

#         response = self.client.get("AccountManagement/")

#         self.assertRedirects(response, "/")

#     def test_instructor_access_account_management(self):
#         instructor_user = User.objects.create_user(
#             email='instructor@example.com',
#             password='instructorpassword123',
#             fname='Instructor',
#             lname='User',
#             address='789 Instructor Lane',
#             phone_number='1239874560'
#         )

#         self.client.login(email='instructor@example.com', password='instructorpassword123')

#         response = self.client.get("AccountManagement/")

#         self.assertRedirects(response, "/")
