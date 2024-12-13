from django.test import TestCase
from django.contrib.auth import get_user_model
from TAScheduler.models import Course, Supervisor
from django.contrib.auth.models import Group

User = get_user_model()

class CreateCourseTests(TestCase):
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

        # Create Supervisor
        self.supervisor = Supervisor.objects.create(
            user=self.supervisor_user,
            admin_dept='Computer Science'
        )

    def test_create_course_no_error(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 200)

        data = {
            'course_name': 'Test Course',
            'course_identifier': '600',
            'course_dept': 'Computer Science',
            'course_credits': 3,
            'action': 'create',
        }
        response = self.client.post("/courses_supervisor/", data)
        self.assertEqual(response.status_code, 302)

        # Check if the course was created successfully
        new_course = Course.objects.get(course_name='Test Course')
        self.assertEqual(new_course.course_name, 'Test Course')
        self.assertEqual(new_course.course_identifier, '600')
        self.assertEqual(new_course.course_dept, 'Computer Science')
        self.assertEqual(new_course.super_id, self.supervisor)

    def test_create_course_no_supervisor(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        response = self.client.get("/courses_supervisor/")
        self.assertEqual(response.status_code, 200)

        # Test missing supervisor field by omitting super_id
        data = {
            'course_name': 'Test Course',
            'course_identifier': '600',
            'course_dept': 'Computer Science',
            'course_credits': 3,
            'action': 'create',
        }
        response = self.client.post("/courses_supervisor/", data)
        new_course = Course.objects.get(course_name='Test Course')
        self.assertEqual(new_course.course_name, 'Test Course')
        self.assertEqual(new_course.course_identifier, '600')
        self.assertEqual(new_course.course_dept, 'Computer Science')


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

    def test_course_identifier_must_be_unique(self):
        self.client.login(email='supervisor@example.com', password='superpassword123')

        #test2
        data1 = {
            'course_name': 'Test Course',
            'course_identifier': '600',
            'course_dept': 'Computer Science',
            'course_credits': 3,
            'action': 'create',
        }

        response1 = self.client.post("/courses_supervisor/", data1)

        data2 = {
            'course_name': 'Other Test Course',
            'course_identifier': '600',
            'course_dept': 'Computer Science',
            'course_credits': 3,
            'action': 'create',
        }
        response2 = self.client.post("/courses_supervisor/", data2)

        courses = Course.objects.filter(course_identifier='600')
        self.assertEqual(courses.count(), 1)

