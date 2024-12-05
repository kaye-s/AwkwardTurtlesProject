from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.auth.models import Group
from TAScheduler.models import Course, Supervisor, Section, Lab, TA

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

        self.testSection = Section(section_num=300, section_course=self.testCourse)
        self.testSection.save()
        self.testLab = Lab(lab_section=self.testSection, lab_ta=self.ta_user, days_of_week="MWF", lab_startTime='2024-11-01-00-00', lab_endTime='2024-11-01-10-00')
        self.testLab.save()

    def test_delete_section_success(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/course/delete_section/" + self.testSection.section_id.__str__() + "/")
        self.assertEqual(response.status_code, 200)

        data = {
            'section_id': self.testSection.section_id,
            'action': 'delete'
        }
        response = self.client.post("/course/", data)
        self.assertEqual(response.status_code, 302)  # status is a type 3XX cause our view redirects back to itself

        checkSection = Section.objects.get(course_id=self.testSection.section_id)
        self.assertIsNone(checkSection)

    def test_delete_section_cascade(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/course/delete_section/" + self.testSection.section_id.__str__() + "/")
        self.assertEqual(response.status_code, 200)

        data = {
            'section_id': self.testSection.section_id,
            'action': 'delete'
        }
        response = self.client.post("/course/", data)
        self.assertEqual(response.status_code, 302)  # status is a type 3XX cause our view redirects back to itself

        checkLab = Lab.objects.get(Lab_id=self.testLab.lab_id)
        self.assertIsNone(checkLab)

        self.assertIsNone(self.testSection)

    def test_delete_section_invalid_course(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/course/delete_section/" + self.testSection.section_id.__str__() + "/")
        self.assertEqual(response.status_code, 200)

        data = {
            'section_id': 12445,
            'action': 'delete'
        }
        response = self.client.post("/course/", data)
        self.assertEqual(response.status_code, 302)  # status is a type 3XX cause our view redirects back to itself

        checkSection = Section.objects.get(course_id=self.testSection.section_id)
        self.assertIsNone(checkSection)

        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(
            any("Cannot delete section, as section does not exist" in str(message) for message in
                messages),
            "Expected a message - section does not exist")

    def test_delete_section_as_TA(self):
        self.client.login(email='ta@uwm.edu', password='tapassword123')

        response = self.client.get("/course/delete_section/" + self.testSection.section_id.__str__() + "/")
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_delete_section_as_Instructor(self):
        self.client.login(email='instructor@uwm.edu', password='instructorpassword123')

        response = self.client.get("/course/delete_section/" + self.testSection.section_id.__str__() + "/")
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
