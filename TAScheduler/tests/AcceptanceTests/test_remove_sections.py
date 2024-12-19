from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.auth.models import Group
from TAScheduler.models import Course, Supervisor, Section, TA

User = get_user_model()


class TestDeleteSections(TestCase):
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

        self.ta_user = User.objects.create_user(
            email='ta@example.com',
            password='tapassword123',
            fname='TA',
            lname='User',
            address='123 TA Lane',
            phone_number='1234567890'
        )
        ta_group, _ = Group.objects.get_or_create(name='TA')
        self.ta_user.groups.add(ta_group)
        self.ta_user = TA(user=self.ta_user, ta_dept="TA Dept")
        self.ta_user.save()

        self.testCourse = Course(super_id=self.supervisor_user, course_name='Test Course', course_identifier="601",
                                 course_dept="Testing Dept", course_credits=3)
        self.testCourse.save()

        self.testSection = Section(section_num=300, section_course=self.testCourse, days_of_week="MFW", section_startTime='8:00', section_endTime="9:00")
        self.testSection.save()

    def test_delete_section_success(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 200)

        data = {
            'section_id': self.testSection.section_id,
            'action': 'deleteSection'
        }

        response = self.client.post("/courses_supervisor/", data)
        self.assertEqual(response.status_code, 302)

        checkSection = Section.objects.filter(section_id=self.testSection.section_id).exists()
        self.assertFalse(checkSection)

    def test_delete_section_cascade(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 200)

        data = {
            'section_id': self.testSection.section_id,
            'action': 'deleteSection'
        }
        response = self.client.post("/courses_supervisor/", data)
        self.assertEqual(response.status_code, 302)

        checkSection = Section.objects.filter(section_id=self.testSection.section_id).exists()
        self.assertFalse(checkSection)

    def test_delete_section_invalid_course(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 200)

        data = {
            'section_id': 12445,
            'action': 'deleteSection'
        }
        response = self.client.post("/courses_supervisor/", data)
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any("Section does not exist" in str(message) for message in
                messages),
            "Expected a message - section does not exist")

    def test_delete_section_as_TA(self):
        self.client.login(email='ta@uwm.edu', password='tapassword123')

        data = {
            'section_id': self.testSection.section_id,
            'action': 'deleteSection'
        }

        response = self.client.post("/courses_supervisor/", data)
        self.assertEqual(response.status_code, 302)

    def test_delete_section_as_Instructor(self):
        self.client.login(email='instructor@uwm.edu', password='instructorpassword123')

        data = {
            'section_id': self.testSection.section_id,
            'action': 'deleteSection'
        }

        response = self.client.post("/courses_supervisor/", data)
        self.assertEqual(response.status_code, 302)
