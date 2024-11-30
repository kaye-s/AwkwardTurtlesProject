# from django.test import TestCase
# from TAScheduler.forms import UserForm, SupervisorAdminForm
# from TAScheduler.models import User, Supervisor

# class UserFormTests(TestCase):
#     def test_user_creation_form_valid(self):
#         form_data = {
#             'email': 'testuser@example.com',
#             'fname': 'John',
#             'lname': 'Doe',
#             'phone_number': '1234567890',
#             'address': '123 Main St',
#             'password1': 'strongpassword',
#             'password2': 'strongpassword',
#         }
#         form = UserForm(data=form_data)
#         self.assertTrue(form.is_valid())
#         user = form.save()
#         self.assertEqual(user.email, 'testuser@example.com')
#         self.assertTrue(user.check_password('strongpassword'))

#     def test_user_creation_form_password_mismatch(self):
#         form_data = {
#             'email': 'testuser@example.com',
#             'fname': 'John',
#             'lname': 'Doe',
#             'phone_number': '1234567890',
#             'address': '123 Main St',
#             'password1': 'megasonicteenagewarhead',
#             'password2': 'differentpassword',
#         }
#         form = UserForm(data=form_data)
#         self.assertFalse(form.is_valid()) #debug into to fix the problem
#         self.assertIn('Passwords do not match.', form.errors['password2'])

# class SupervisorAdminFormTests(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email="supervisor@example.com",
#             password="password123",
#             fname="Jane",
#             lname="Doe"
#         )

#     def test_supervisor_creation(self):
#         form_data = {'user': self.user.email, 'admin_dept': 'Computer Science'}
#         form = SupervisorAdminForm(data=form_data)
#         self.assertTrue(form.is_valid())
#         supervisor = form.save()
#         self.assertEqual(supervisor.user, self.user)
#         self.assertEqual(supervisor.admin_dept, 'Computer Science')