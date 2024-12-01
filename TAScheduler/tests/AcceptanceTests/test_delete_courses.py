from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.auth.models import Group
from TAScheduler.models import Course, Supervisor, Section

User = get_user_model()

class TestDeleteCourses(TestCase):
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
        self.supervisor_user = Supervisor(user=self.supervisor_user, admin_dept="Supervisor Dept")
        self.supervisor_user.save()

        self.testCourse = Course(super_id=self.supervisor_user, course_name='Test Course', course_identifier="601", course_dept="Testing Dept", course_credits=3)
        self.testCourse.save()

        self.testSection = Section(section_num=300, section_course=self.testCourse)
        self.testSection.save()

    def test_delete_course_success(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 200)


        data = {
            'course_id': self.testCourse.course_id,
            'action': 'delete'
        }
        response = self.client.post("/courses_supervisor/", data)
        self.assertEqual(response.status_code, 302)  # status is a type 3XX cause our view redirects back to itself

        checkCourse = Course.objects.filter(course_id=self.testCourse.course_id).exists()
        self.assertFalse(checkCourse)

    def test_delete_course_cascade(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 200)

        data = {
            'course_id': self.testCourse.course_id,
            'action': 'delete'
        }
        response = self.client.post("/courses_supervisor/", data)
        self.assertEqual(response.status_code, 302)  # status is a type 3XX cause our view redirects back to itself

        checkCourse = Course.objects.filter(course_id=self.testCourse.course_id).exists()
        self.assertFalse(checkCourse)

        checkSection = Section.objects.filter(section_num=300).exists()
        self.assertFalse(checkSection)

    def test_delete_course_invalid_course(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 200)

        data = {
            'course_id': 12445,
            'action': 'delete'
        }
        response = self.client.post("/courses_supervisor/", data)
        self.assertEqual(response.status_code, 302)  # status is a type 3XX cause our view redirects back to itself

        checkCourse = Course.objects.get(course_id=self.testCourse.course_id)
        self.assertIsNone(checkCourse)

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any("Cannot delete course, as course does not exist" in str(message) for message in
                messages),
            "Expected a message - course does not exist")

    def test_delete_course_as_TA(self):
        self.client.login(email='ta@uwm.edu', password='tapassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_delete_course_as_Instructor(self):
        self.client.login(email='instructor@uwm.edu', password='instructorpassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
