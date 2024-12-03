from django.test import TestCase, Client
from TAScheduler.models import Course, Supervisor, User


class CourseViewTests(TestCase):
    def test_add_course_valid(self):
        supervisor_user = User.objects.create_user(
            email="supervisor@example.com",
            password="password123",
            fname="John",
            lname="Doe",
            is_superuser=True
        )
        supervisor = Supervisor.objects.create(user=supervisor_user, admin_dept="Computer Science")

        # Add user to Supervisor group
        from django.contrib.auth.models import Group
        group = Group.objects.get(name="Supervisor")
        supervisor_user.groups.add(group)
        supervisor_user.save()

        client = Client()
        client.login(email="supervisor@example.com", password="password123")

        response = client.post("/create_course/", {
            'course_name': 'Intro to Computer Science',
            'course_identifier': 'CS101',
            'course_dept': 'Computer Science',
            'course_credits': 3
        })

        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(response, "/courses_supervisor/")  # Replace with actual redirect URL
        self.assertTrue(Course.objects.filter(course_name="Intro to Computer Science", course_identifier="CS101").exists())

    def test_delete_course_valid(self):
        # Creating a supervisor user to test course deletion
        supervisor_user = User.objects.create_user(
            email="supervisor@example.com",
            password="password123",
            fname="John",
            lname="Doe",
            is_superuser=True
        )
        supervisor = Supervisor.objects.create(user=supervisor_user, admin_dept="Computer Science")

        # Creating a course to delete
        course = Course.objects.create(
            super_id=supervisor,
            course_name='Intro to Programming',
            course_identifier='CS100',
            course_dept='Computer Science',
            course_credits=3
        )

        # Logging in as the supervisor
        client = Client()
        client.login(email="supervisor@example.com", password="password123")

        # Attempt to delete the course
        response = client.post(f"/delete_course/{course.course_id}/")  # works with using course.course_id
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(response, "/courses_supervisor/")  # replaced with actual redirect URL
        self.assertFalse(Course.objects.filter(course_id=course.course_id).exists())  # Use course.course_id