#Changed from error to failing

from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.auth.models import Group

from TAScheduler.models import Section, Course, Supervisor

User = get_user_model()


class CreateSectionsTests(TestCase):
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

        self.new_sup = Supervisor(user=self.supervisor_user, admin_dept="Maths")
        self.new_sup.save()

        self.test_course_valid = Course(super_id=self.new_sup, course_name='Test Course', course_identifier=600, course_dept='Test Course Department', course_credits=33)
        self.test_course_valid.save()
        self.test_course_invalid = Course.DoesNotExist

    def test_create_section_no_error(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/course-supervisor/")
        self.assertEqual(response.status_code, 200)

        data = {
            'section_num': '733',
            'section_course': self.test_course_valid,
            'action': 'create',
        }
        response = self.client.post("/course-supervisor/", data)
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))

        self.assertEquals(len(messages), 0)

    def test_create_section_no_course(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/course-supervisor/")
        self.assertEqual(response.status_code, 200)

        data = {
            'section_num': '733',
            'action': 'create',
        }
        response = self.client.post("/course-supervisor/", data)
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any("Parent course cannot be empty" in str(message) for message in messages),
            "Expected message about parent course not found in the session messages.")

    def test_create_section_invalid_course(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/course-supervisor/")
        self.assertEqual(response.status_code, 200)

        data = {
            'section_num': '733',
            'section_course': self.test_course_invalid,
            'action': 'create',
        }
        response = self.client.post("/course-supervisor/", data)
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any("Course must be a valid course within the database" in str(message) for message in messages),
            "Expected message about course not found not found in the session messages.")

    def test_create_section_duplicate_course_same_section(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/course-supervisor/")
        self.assertEqual(response.status_code, 200)

        data = {
            'section_num': '733',
            'section_course': self.test_course_valid,
            'action': 'create',
        }
        response = self.client.post("/course-supervisor/", data)
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))

        self.assertEquals(len(messages), 0)

        new_course = Section.objects.get(course_id=1)
        self.assertIsNotNone(new_course)
        self.assertEqual(new_course.course_name, 'Test Course')

        data = {
            'section_num': '733',
            'section_course': self.test_course_valid,
            'action': 'create',
        }
        response = self.client.post("/course-supervisor/", data)
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any("Cannot choose the same section number as another section in the course" in str(message) for message in messages),
            "Expected message about section number being a duplicate within the same course not found not found in the session messages.")

    def test_instructor_access_section_management(self):
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


    def test_ta_access_section_management(self):
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



