from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.auth.models import Group

from TAScheduler.models import Course

User = get_user_model()


class CreateCourseTests(TestCase):
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


    def test_create_course_no_error(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/course-supervisor/")
        self.assertEqual(response.status_code, 200)

        data = {
            'super_id': 'self.supervisor_user',
            'course_name': 'Test Course',
            'course_identifier': 600,
            'course_description': 'Test Course Department',
            'course_credits': 33,
            'action': 'create',
        }
        response = self.client.post("/course-supervisor/", data)
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))

        self.assertEquals(len(messages), 0)


    def test_create_course_no_supervisor(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/course-supervisor/")
        self.assertEqual(response.status_code, 200)

        data = {
            'course_name': 'Test Course',
            'course_identifier': 600,
            'course_description': 'Test Course Department',
            'course_credits': 33,
            'action': 'create',
        }
        response = self.client.post("/course-supervisor/", data)
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any("Supervisor cannot be empty" in str(message) for message in messages),
            "Expected message about missing supervisor not found in the session messages.")

    def test_create_course_invalid_supervisor(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/course-supervisor/")
        self.assertEqual(response.status_code, 200)

        data = {
            'super_id': 'invalid-super-id',
            'course_name': 'Test Course',
            'course_identifier': 600,
            'course_description': 'Test Course Department',
            'course_credits': 33,
            'action': 'create',
        }
        response = self.client.post("/course-supervisor/", data)
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any("Supervisor must be a valid supervisor" in str(message) for message in messages),
            "Expected message about invalid supervisor not found in the session messages.")

    def test_instructor_access_course_management(self):
        User.objects.create_user(
            email='instructor@example.com',
            password='instructorpassword123',
            fname='Instructor',
            lname='User',
            address='789 Instructor Lane',
            phone_number='1239874560'
        )
        self.client.login(email='instructor@example.com', password='instructorpassword123')

        response = self.client.get("/course-supervisor/")

        self.assertEqual(response, "/course/")


    def test_ta_access_course_management(self):
        User.objects.create_user(
            email='ta@example.com',
            password='tapassword123',
            fname='TA',
            lname='User',
            address='789 Teaching Assistant Lane',
            phone_number='1239874560'
        )
        self.client.login(email='ta@example.com', password='tapassword123')

        response = self.client.get("/course-supervisor/")

        self.assertEqual(response, "/course/")



    







