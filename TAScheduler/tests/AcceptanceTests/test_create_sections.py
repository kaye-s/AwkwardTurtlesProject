from datetime import datetime, time

from django.test import TestCase
from django.contrib.auth import get_user_model
from TAScheduler.models import Course, Supervisor, TA, Instructor, Section
from django.contrib.auth.models import Group
from django.contrib.messages import get_messages

User = get_user_model()

class CreateSectionTests(TestCase):
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

        self.course_test2 = Course.objects.create(
            super_id=self.supervisor_user,
            course_name='CS250',
            course_identifier='250',
            course_dept='Computer Science',
            course_credits=3,
        )
        self.course_test2.save()

    def test_create_section_no_error_no_users(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 200)

        data = {
            'course_id': self.course_test.course_id,
            'section_type': 'Lab',
            'section_num': '600',
            'section_course': self.course_test,
            'days_of_week': 'MW',
            'section_startTime': '08:00',
            'section_endTime': '10:00',
            'action': 'createSection',
        }
        response = self.client.post("/courses_supervisor/", data)
        self.assertEqual(response.status_code, 302)

        # Check if the section was created successfully
        new_section = Section.objects.get(section_num='600')
        self.assertEqual(new_section.section_type, 'Lab')
        self.assertEqual(new_section.section_num, 600)
        self.assertEqual(new_section.section_course, self.course_test)
        self.assertEqual(new_section.days_of_week, 'MW')
        self.assertEqual(new_section.section_startTime, time(8, 0))
        self.assertEqual(new_section.section_endTime, time(10, 0))

    def test_instructor_access_course_management(self):
        self.client.login(email='instructor@example.com', password='instructorpassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 403)

    def test_ta_access_course_management(self):
        self.client.login(email='ta@example.com', password='tapassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 403)

    def test_section_identifier_must_be_unique(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 200)

        data = {
            'course_id': self.course_test.course_id,
            'section_type': 'Lab',
            'section_num': '600',
            'section_course': self.course_test,
            'days_of_week': 'MW',
            'section_startTime': '08:00',
            'section_endTime': '10:00',
            'action': 'createSection',
        }
        response = self.client.post("/courses_supervisor/", data)
        self.assertEqual(response.status_code, 302)

        data2 = {
            'course_id': self.course_test2.course_id,
            'section_type': 'Lab',
            'section_num': '600',
            'section_course': self.course_test2,
            'days_of_week': 'MW',
            'section_startTime': '08:00',
            'section_endTime': '10:00',
            'action': 'createSection',
        }
        response = self.client.post("/courses_supervisor/", data2)
        self.assertEqual(response.status_code, 302)

        new_section = Section.objects.get(section_num=600)
        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any(f"A section with the identifier '{new_section.section_num}' already exists." in str(message) for
                message in
                messages),
            "Expected a message - section ID already exists")
        sections = Section.objects.filter(section_num=600)
        self.assertEqual(sections.count(), 1)


