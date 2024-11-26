from django.test import TestCase, Client
from TAScheduler.models import Course, Supervisor, User


class CourseViewTests(TestCase):
    def test_add_course_valid(self):

            # creating a supervisor user to test adding course
            supervisor_user = User.objects.create_user(
                email="supervisor@example.com",
                password="password123",
                fname="John",
                lname="Doe",
                is_superuser=True
            )
            supervisor = Supervisor.objects.create(user=supervisor_user, admin_dept="Computer Science")

            # logging in as the supervisor we created
            client = Client()
            client.login(email="supervisor@example.com", password="password123")

            # Test adding a valid course
            response = client.post("/", {  #need actual url for the course page.. in lab we just use / for root
                'super_id': supervisor.id,
                'course_name': 'Intro to Computer Science',
                'course_identifier': 'CS101',
                'course_dept': 'Computer Science',
                'course_credits': 3
            })
            self.assertEqual(response.status_code, 200)
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
        response = client.post("/", {  # Using "/" for now
            'action': 'delete_course',
            'course_id': course.id
        })
        # Replace with the correct URL for deleting a course
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Course.objects.filter(id=course.id).exists())
