from django.test import TestCase
from django.contrib.auth.models import Permission
from TAScheduler.models import User, Supervisor

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



