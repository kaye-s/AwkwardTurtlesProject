from django.test import TestCase, Client
from django.urls import reverse
from TAScheduler.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class ContactInfoUpdateTests(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            fname="Test",
            lname="User",
            address="123 Main St",
            phone_number="1234567890"
        )
        self.client = Client()
        self.update_url = reverse('contact-info')

    def test_update_contact_info_success(self):

        self.client.login(email="testuser@example.com", password="password123")
        new_data = {
            'fname': 'Updated',
            'lname': 'User',
            'email': 'updateduser@example.com',
            'address': '456 New St',
            'phone_number': '0987654321'
        }

        response = self.client.post(self.update_url, new_data)

        self.user.refresh_from_db()

        self.assertEqual(self.user.fname, 'Updated')
        self.assertEqual(self.user.lname, 'User')
        self.assertEqual(self.user.email, 'updateduser@example.com')
        self.assertEqual(self.user.address, '456 New St')
        self.assertEqual(self.user.phone_number, '0987654321')

        self.assertRedirects(response, self.update_url)


    def test_partial_update_contact_info(self):

        self.client.login(email="testuser@example.com", password="password123")

        new_data = {
            'phone_number': '1112223333'
        }

        response = self.client.post(self.update_url, new_data)


        self.user.refresh_from_db()

        # see if tthe phone number was updated
        self.assertEqual(self.user.phone_number, '1112223333')
        self.assertEqual(self.user.fname, 'Test')
        self.assertEqual(self.user.address, '123 Main St')

        self.assertRedirects(response, self.update_url)

    def test_other_user_contact_info_not_affected(self):

        other_user = User.objects.create_user(
            email="otheruser@example.com",
            password="password456",
            fname="Other",
            lname="User",
            address="789 Other St",
            phone_number="5555555555"
        )

        self.client.login(email="testuser@example.com", password="password123")

        # update contact info for  first user
        new_data = {
            'fname': 'Updated',
            'address': 'New Address'
        }
        self.client.post(self.update_url, new_data)

        self.user.refresh_from_db()
        other_user.refresh_from_db()

        #  make sure that the first user's info was updated
        self.assertEqual(self.user.fname, 'Updated')
        self.assertEqual(self.user.address, 'New Address')

        #check to see if second user's info is unchanged

        self.assertEqual(other_user.fname, 'Other')
        self.assertEqual(other_user.address, '789 Other St')
