
from django.test import TestCase
from django.contrib.auth.models import Permission
from TAScheduler.models import User, Supervisor, Course


class SupervisorModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="supervisor@example.com",
            password="password123",
            fname="John",
            lname="Doe"
        )
        self.supervisor = Supervisor.objects.create(
            user=self.user,
            admin_dept="Computer Science"
        )

    def test_supervisor_creation(self):
        self.assertEqual(self.supervisor.user.email, "supervisor@example.com")
        self.assertEqual(self.supervisor.admin_dept, "Computer Science")

    def test_supervisor_permissions(self):
        permissions = self.user.get_all_permissions()
        self.assertIn('TAScheduler.create_courses', permissions)
        self.assertIn('TAScheduler.assign_instructors', permissions)


class CourseToSupervisorModelTests(TestCase):
    def setUp(self):
        self.firstUser1 = User.objects.create_user(
            email="supervisor@example.com",
            password="blank123",
            fname="John",
            lname="Doe",
            address='1234 Oaklane Rd',
            phone_number='123-456-7890'
        )
        self.supervisor1 = Supervisor.objects.create(
            user=self.firstUser1,  # Fixed assignment
            admin_dept='Engineering'
        )
        self.course1 = Course.objects.create(
            super_id=self.supervisor1,  # Assuming this uses the correct ForeignKey
            course_name='Engineer 101',
            course_identifier='601',
            course_dept='Engineering',
            course_credits=3
        )

    def testForeignKeyConnection(self):
        self.assertEqual(self.firstUser1.email, self.supervisor1.user.email)  # Access the email attribute
        self.assertEqual(self.supervisor1.id, self.course1.super_id.id)  # Assuming super_id is a ForeignKey

    def testAccessThoughFK(self):
        # Adjust the test based on actual ForeignKey setup
        self.assertEqual(self.course1.super_id.user.email, self.firstUser1.email)

    def testModifyingValues(self):
        self.firstUser1.fname = "Sally"  # Fixed assignment
        self.firstUser1.save()  # Make sure changes are saved
        self.assertEqual(User.objects.get(pk=self.firstUser1.pk).fname, "Sally")  # Query the updated value


class CourseTests(TestCase):
    def setUp(self):
        self.firstUser1 = User.objects.create_user(
            email="supervisor@example.com",
            password="blank123",
            fname="John",
            lname="Doe",
            address='1234 Oaklane Rd',
            phone_number='123-456-7890'
        )
        self.supervisor1 = Supervisor.objects.create(
            user=self.firstUser1,  # Fixed assignment
            admin_dept='Engineering'
        )
        self.course1 = Course.objects.create(
            super_id=self.supervisor1,  # Assuming this uses the correct ForeignKey
            course_name='Engineer 101',
            course_identifier='601',
            course_dept='Engineering',
            course_credits=3
        )

    def testInitalValues(self):
        self.assertEqual(self.course1.super_id.user.email, "supervisor@example.com")  # Adjusted to check email
        self.assertEqual(self.course1.course_name, "Engineer 101")
        self.assertEqual(self.course1.course_identifier, "601")
        self.assertEqual(self.course1.course_dept, "Engineering")
        self.assertEqual(self.course1.course_credits, 3)

    def testModifyingValues(self):
        self.course1.super_id = self.supervisor1  # Fixed assignment with actual instance
        self.assertEqual(self.course1.super_id, self.supervisor1)
        self.course1.course_name = "Math Course"
        self.course1.save()  # Save the changes
        self.assertEqual(Course.objects.get(pk=self.course1.pk).course_name, "Math Course")  # Query the updated value
        self.course1.course_identifier = "101"
        self.course1.save()
        self.assertEqual(Course.objects.get(pk=self.course1.pk).course_identifier, "101")
        self.course1.course_dept = "Mathematics"
        self.course1.save()
        self.assertEqual(Course.objects.get(pk=self.course1.pk).course_dept, "Mathematics")
        self.course1.course_credits = 5
        self.course1.save()
        self.assertEqual(Course.objects.get(pk=self.course1.pk).course_credits, 5)