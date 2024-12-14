from django.test import TestCase, Client
from django.urls import reverse
from TAScheduler.models import Supervisor, Instructor, TA
from django.contrib.auth.models import User

class UserContactInfoAcceptanceTest(TestCase):

    def setUp(self):
        """Set up the test environment."""
        # Create users
        self.supervisor = User.objects.create_user(username='supervisor', password='password', email='supervisor@example.com')
        self.instructor = User.objects.create_user(username='instructor', password='password', email='instructor@example.com')
        self.ta = User.objects.create_user(username='ta', password='password', email='ta@example.com')
        
        # Add users to respective roles
        Supervisor.objects.create(user=self.supervisor)
        Instructor.objects.create(user=self.instructor)
        TA.objects.create(user=self.ta)

        # Client setup
        self.client = Client()
        self.user_contact_info_url = reverse('user-contact-info', kwargs={"username": self.ta.username})

    def test_access_contact_info_page_authenticated(self):
        """Test that the contact info page is accessible for an authenticated supervisor."""
        # Login as supervisor
        self.client.login(username='supervisor', password='password')
        response = self.client.get(self.user_contact_info_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'UserContactInfo.html')  # Ensure correct template is used

    def test_contact_info_displayed_correctly(self):
        """Test that user contact information is displayed properly."""
        self.client.login(username='supervisor', password='password')
        response = self.client.get(self.user_contact_info_url)
        self.assertContains(response, "ta")  # Username
        self.assertContains(response, "ta@example.com")  # Email

    def test_unauthorized_user_access(self):
        """Test that unauthorized users cannot access the contact info page."""
        # Logout supervisor and try accessing as a guest
        self.client.logout()
        response = self.client.get(self.user_contact_info_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        
        # Login as TA and test restricted access
        self.client.login(username='ta', password='password')
        response = self.client.get(self.user_contact_info_url)
        self.assertEqual(response.status_code, 403)  # Forbidden for TAs

    def test_invalid_user_contact_page(self):
        """Test accessing a contact page for a non-existent user."""
        self.client.login(username='supervisor', password='password')
        invalid_url = reverse('user-contact-info', kwargs={"username": "invalid_user"})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)  # Page not found
