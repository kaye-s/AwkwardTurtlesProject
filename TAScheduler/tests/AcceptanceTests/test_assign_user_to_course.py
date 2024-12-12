from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.auth.models import Group

from TAScheduler.models import Course

User = get_user_model()


class AssignUserToCourseTests(TestCase):

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

        self.instructor_user = User.objects.create_user(
            email='instructor@example.com',
            password='instructorpassword123',
            fname='Instructor',
            lname='User',
            address='456 Instructor Road',
            phone_number='1231231212'
        )

        self.ta_user.save()

        self.course_test = Course.objects.create(
            course_id=1,
            super_id=self.supervisor_user.id,
            course_name='Test Course',
            course_identifier='600',
            course_dept='Computer Science',
            course_credits=3,
        )

        self.course_test.save()

    def test_assign_TA_successful(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 200)

        # Not sure exactly how to refer to a specific user yet, maybe a drop down menu situaiton would be better?
        data = {
            'course_id': 1,
            'course_user': self.ta_user.email,
        }

        response = self.client.post("/courses_supervisor/", data)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.course_test.course_user, 'ta@example.com')

    def test_assign_Instructor_successful(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 200)

        # Not sure exactly how to refer to a specific user yet, maybe a drop down menu situaiton would be better?
        data = {
            'course_id': 1,
            'course_user': self.instructor_user.email,
        }

        response = self.client.post("/courses_supervisor/", data)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.course_test.course_user, 'instructor@example.com')

    def test_assign_User_does_not_exist(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 200)

        # Not sure exactly how to refer to a specific user yet, maybe a drop down menu situaiton would be better?
        data = {
            'course_id': 1,
            'course_user': 'incomplete@example.com',
        }

        response = self.client.post("/courses_supervisor/", data)
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any("This user is not in the database, cannot assign course" in str(message) for message in
                messages),
            "Expected a message - user is not in the system")

    def test_assign_Course_does_not_exist(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 200)

        # Not sure exactly how to refer to a specific user yet, maybe a drop down menu situaiton would be better?
        data = {
            'course_id': 1,
            'course_user': 'ta@example.com',
        }

        response = self.client.post("/courses_supervisor/", data)
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any("This course is not in the database, cannot assign user" in str(message) for message in
                messages),
            "Expected a message - course is not in the system")

    def test_assign_nothing(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 200)

        # Not sure exactly how to refer to a specific user yet, maybe a drop down menu situaiton would be better?
        data = {
            'course_id': 1,
        }

        response = self.client.post("/courses_supervisor/", data)
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any("Please enter a user to assign to this course" in str(message) for message in
                messages),
            "Expected a message - please fill in all boxes")

    def test_instructor_access_course_management(self):
        self.client.login(email='instructor@example.com', password='instructorpassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 403)

    def test_ta_access_course_management(self):
        self.client.login(email='ta@example.com', password='tapassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 403)