from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.auth.models import Group
from TAScheduler.models import Course, Supervisor, Section, Instructor, TA

User = get_user_model()

class TestDeleteCourses(TestCase):
    def setUp(self):
        # Create Supervisor User
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
        self.supervisor_user = Supervisor(user=self.supervisor_user, admin_dept="dept")
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
        self.ta_user = TA(user=self.ta_user, ta_dept="dept")
        self.ta_user.save()

        self.instructor_user = User.objects.create_user(
            email='instructor@example.com',
            password='instructorpassword123',
            fname='Instructor',
            lname='User',
            address='456 TA Road',
            phone_number='0987654321'
        )

        self.instructor_user.save()
        self.instructor_user = Instructor(user=self.instructor_user, instructor_dept="dept")
        self.instructor_user.save()

        self.course_test = Course.objects.create(
            super_id=self.supervisor_user,
            course_name='CS150',
            course_identifier='150',
            course_dept='Computer Science',
            course_credits=3,
        )
        self.course_test.save()

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

        #checkCourse = Course.objects.get(course_id=self.testCourse.course_id)
        #self.assertIsNone(checkCourse)

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any("Cannot delete course, as course does not exist" in str(message) for message in
                messages),
            "Expected a message - course does not exist")

    def test_ta_access_course_management(self):
        # Create TA User
        ta_user = User.objects.create_user(
            email='ta@example.com',
            password='tapassword123',
            fname='TA',
            lname='User',
            address='789 TA Lane',
            phone_number='1239874560'
        )
        self.client.login(email='ta@example.com', password='tapassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 403)

    def test_instructor_access_course_management(self):
        # Create Instructor User
        instructor_user = User.objects.create_user(
            email='instructor@example.com',
            password='instructorpassword123',
            fname='Instructor',
            lname='User',
            address='789 Instructor Lane',
            phone_number='1239874560'
        )
        self.client.login(email='instructor@example.com', password='instructorpassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 403)