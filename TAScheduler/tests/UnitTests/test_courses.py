from cgitb import reset

from django.test import TestCase
from unittest.mock import MagicMock, patch
from django.contrib.auth.models import User
from django.contrib import messages
from TAScheduler.models import Supervisor, TA, Instructor, Course
from TAScheduler.utils.account_management import create_user_account, edit_user_account, delete_user_account
from django.urls import reverse
from django.contrib.auth import get_user_model

from TAScheduler.utils.courses import *

User = get_user_model()

class AccountManagementCreateTests(TestCase):

    def setUp(self):
        self.url = reverse('courses-supervisor')
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
            course_name='CS600',
            course_identifier='600',
            course_dept='Computer Science',
            course_credits=3,
        )
        self.course_test.save()

    @patch('django.contrib.messages.error')
    def test_create_course_success(self, mock_message):
        post_data = {
            'course_name': 'Test Course',
            'course_identifier': '150',
            'course_dept': 'Computer Science',
            'course_credits': 3,
        }

        request = MagicMock()
        request.POST = post_data
        request.user = self.supervisor_user.user

        create_course(request)

        course = Course.objects.get(course_name='Test Course')

        # Assert course is created
        self.assertEqual(course.course_name, 'Test Course')
        self.assertEqual(course.course_identifier, '150')

        # Assert no errors in case of success
        mock_message.assert_not_called()

    @patch('django.contrib.messages.error')
    def test_create_course_success_instructor(self, mock_message):
        post_data = {
            'course_name': 'Test Course',
            'course_identifier': '150',
            'course_dept': 'Computer Science',
            'course_credits': 3,
            'instructor': self.instructor_user.user
        }

        request = MagicMock()
        request.POST = post_data
        request.user = self.supervisor_user.user

        create_course(request)

        course = Course.objects.get(course_name='Test Course')

        # Assert course is created
        self.assertEqual(course.course_name, 'Test Course')
        self.assertEqual(course.course_identifier, '150')
        self.assertEqual(course.instructor, self.instructor_user)

        # Assert no errors in case of success
        mock_message.assert_not_called()

    @patch('django.contrib.messages.error')
    def test_create_course_no_identifier(self, mock_message):
        post_data = {
            'course_name': 'Test Course',
            'course_identifier': '600',
            'course_dept': 'Computer Science',
            'course_credits': 3,
            'instructor': self.instructor_user.user

        }

        request = MagicMock()
        request.POST = post_data
        request.user = self.supervisor_user.user

        create_course(request)

        mock_message.assert_called_with(request, f"A course with the identifier '{post_data['course_identifier']}' already exists.")

    @patch('django.contrib.messages.error')
    def test_edit_course_success(self, mock_message):
        post_data = {
            'course_dept': 'Robotics',
            'course_credits': 3,
            'instructor': self.instructor_user.user

        }

        request = MagicMock()
        request.POST = post_data
        request.user = self.supervisor_user.user

        edit_course(request, self.course_test.course_id,)

        course = Course.objects.get(course_name='CS600')

        # Assert course is created
        self.assertEqual(course.course_name, 'Test Course')
        self.assertEqual(course.course_identifier, '150')