from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.auth.models import Group

from TAScheduler.models import Course, Supervisor, TA

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

        self.ta2_user = User.objects.create_user(
            email='ta2@example.com',
            password='tapassword123',
            fname='TA2',
            lname='User',
            address='456 TA Road',
            phone_number='0987654321'
        )

        self.ta2_user.save()
        self.ta2_user = TA(user=self.ta2_user, ta_dept="dept")
        self.ta2_user.save()

        self.course_test = Course.objects.create(
            super_id=self.supervisor_user,
            course_name='Test Course',
            course_identifier='600',
            course_dept='Computer Science',
            course_credits=3,
        )

        self.instructor_user = User.objects.create_user(
            email='instructor@example.com',
            password='instructorpassword123',
            fname='Instructor',
            lname='User',
            address='456 TA Road',
            phone_number='0987654321'
        )

        self.instructor_user.save()

        self.course_test.save()

    def test_assign_ta_to_course(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')
        data = {
            'course_id': self.course_test.course_id,
            'course_ta': self.ta_user.id,
            'action': 'addTACourse'
        }
        response = self.client.post("/courses_supervisor/", data)
        self.course_test.refresh_from_db()
        self.assertIn(self.ta_user, self.course_test.course_ta.all())

        self.assertEqual(response.status_code, 302)

    def test_assign_multiple_tas(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')
        data = {
            'course_id': self.course_test.course_id,
            'course_ta': self.ta_user.id,
            'action': 'addTACourse'
        }
        response = self.client.post("/courses_supervisor/", data)
        self.course_test.refresh_from_db()
        self.assertIn(self.ta_user, self.course_test.course_ta.all())

        data = {
            'course_id': self.course_test.course_id,
            'course_ta': self.ta2_user.id,
            'action': 'addTACourse'
        }
        response = self.client.post("/courses_supervisor/", data)
        self.course_test.refresh_from_db()
        self.assertIn(self.ta2_user, self.course_test.course_ta.all())

        self.assertEqual(response.status_code, 302)

    def test_remove_ta_from_course(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')
        data = {
            'course_id': self.course_test.course_id,
            'course_ta': self.ta_user.id,
            'action': 'addTACourse'
        }
        response = self.client.post("/courses_supervisor/", data)
        self.course_test.refresh_from_db()
        self.assertIn(self.ta_user, self.course_test.course_ta.all())

        data = {
            'course_id': self.course_test.course_id,
            'course_ta': self.ta_user.id,
            'action': 'deleteTACourse'
        }
        response = self.client.post("/courses_supervisor/", data)
        self.course_test.refresh_from_db()
        self.assertNotIn(self.ta_user, self.course_test.course_ta.all())

        self.assertEqual(response.status_code, 302)

    def test_ta_already_assigned(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')
        data = {
            'course_id': self.course_test.course_id,
            'course_ta': self.ta_user.id,
            'action': 'addTACourse'
        }
        response = self.client.post("/courses_supervisor/", data)
        self.course_test.refresh_from_db()
        self.assertIn(self.ta_user, self.course_test.course_ta.all())

        data = {
            'course_id': self.course_test.course_id,
            'course_ta': self.ta_user.id,
            'action': 'addTACourse'
        }
        response = self.client.post("/courses_supervisor/", data)

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any("TA already assigned to this course" in str(message) for message in
                messages),
            "Expected a message - TA already assigned")

        self.assertEqual(response.status_code, 302)

    def test_instructor_access_course_management(self):
        self.client.login(email='instructor@example.com', password='instructorpassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 403)

    def test_ta_access_course_management(self):
        self.client.login(email='ta@example.com', password='tapassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 403)