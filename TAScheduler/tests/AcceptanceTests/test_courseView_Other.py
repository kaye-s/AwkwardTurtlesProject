from django.test import TestCase, Client
from django.urls import reverse
from TAScheduler.models import Course, Supervisor, Instructor, TA
from django.contrib.auth.models import User

class CourseViewOtherAcceptanceTest(TestCase):

    def setUp(self):
        """Set up test environment"""
        # Create a Supervisor user
        self.supervisor = User.objects.create_user(username='supervisor', password='password')
        self.supervisor_group = Supervisor.objects.create(user=self.supervisor)

        # Create a course
        self.course = Course.objects.create(name="Test Course", code="CS101", description="Test Description")

        # Create instructors and TAs
        self.instructor = Instructor.objects.create(user=User.objects.create_user(username="instructor", password="password"))
        self.ta = TA.objects.create(user=User.objects.create_user(username="ta", password="password"))

        # Assign client and login as supervisor
        self.client = Client()
        self.client.login(username='supervisor', password='password')

        # URLs
        self.course_view_url = reverse('course-view-other', kwargs={"course_id": self.course.id})  # Example URL
        self.assign_instructor_url = reverse('assign-instructor', kwargs={"course_id": self.course.id})
        self.assign_ta_url = reverse('assign-ta', kwargs={"course_id": self.course.id})

    def test_access_course_view(self):
        """Test that the course view page is accessible."""
        response = self.client.get(self.course_view_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'CourseViewOther.html')  # Adjust template name as needed

    def test_view_course_details(self):
        """Test that course details are displayed correctly."""
        response = self.client.get(self.course_view_url)
        self.assertContains(response, "Test Course")
        self.assertContains(response, "CS101")
        self.assertContains(response, "Test Description")

    def test_assign_instructor(self):
        """Test assigning an instructor to a course."""
        response = self.client.post(self.assign_instructor_url, {"instructor_id": self.instructor.id})
        self.assertEqual(response.status_code, 302)  # Should redirect after assignment
        self.course.refresh_from_db()
        self.assertEqual(self.course.instructor, self.instructor)

    def test_assign_ta(self):
        """Test assigning a TA to a course."""
        response = self.client.post(self.assign_ta_url, {"ta_id": self.ta.id})
        self.assertEqual(response.status_code, 302)  # Should redirect after assignment
        self.course.refresh_from_db()
        self.assertIn(self.ta, self.course.tas.all())

    def test_access_restricted_to_supervisor(self):
        """Test that only supervisors can access the course view page."""
        self.client.logout()
        instructor_client = Client()
        instructor_client.login(username='instructor', password='password')
        response = instructor_client.get(self.course_view_url)
        self.assertEqual(response.status_code, 403)  # Forbidden

        ta_client = Client()
        ta_client.login(username='ta', password='password')
        response = ta_client.get(self.course_view_url)
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_invalid_course_access(self):
        """Test accessing a course that does not exist."""
        invalid_course_url = reverse('course-view-other', kwargs={"course_id": 999})  # Non-existent course ID
        response = self.client.get(invalid_course_url)
        self.assertEqual(response.status_code, 404)
