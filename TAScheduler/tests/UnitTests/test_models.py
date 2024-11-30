# from django.test import TestCase
# from django.contrib.auth.models import Permission
# from TAScheduler.models import User, Supervisor

# class SupervisorModelTests(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email="supervisor@example.com",
#             password="password123",
#             fname="John",
#             lname="Doe"
#         )
#         self.supervisor = Supervisor.objects.create(
#             user=self.user,
#             admin_dept="Computer Science"
#         )

#     def test_supervisor_creation(self):
#         self.assertEqual(self.supervisor.user.email, "supervisor@example.com")
#         self.assertEqual(self.supervisor.admin_dept, "Computer Science")

#     def test_supervisor_permissions(self):
#         permissions = self.user.get_all_permissions()
#         self.assertIn('TAScheduler.create_courses', permissions)
#         self.assertIn('TAScheduler.assign_instructors', permissions)
        
# class CourseToSupervisorModelTests(TestCase):
#     def setUp(self):
#         self.firstUser1 = User(email="supervisor@example.com", password="blank123", fname="John", lname="Doe", address='1234 Oaklane Rd', phone_number='123-456-7890')
#         self.firstUser1.save()
#         self.supervisor1 = Supervisor(user='firstUser', admin_dept='Engineering')
#         self.supervisor1.save()
#         self.course1 = Course(super_id='supervisor', course_name='Engineer 101', course_identifier='601', course_dept='Engineering', course_credits=3)
#         self.course1.save()

#     def testForeignKeyConnection(self):
#         self.assertEqual(self.firstUser1.email, self.supervisor1.user)
#         self.assertEqual(self.supervisor1.id, self.course1.super_id)

#     def testAccessThoughFK(self):
#         self.assertEqual(self.course1.user.email, self.firstUser1.email)
    
#     def testModifyingValues(self):
#         self.course1.user.fname = "Sally"
#         self.assertEqual(self.firstUser1.fname, "Sally")

# class CourseTests(TestCase):
#     def setUp(self):
#         self.firstUser1 = User(email="supervisor@example.com", password="blank123", fname="John", lname="Doe", address='1234 Oaklane Rd', phone_number='123-456-7890')
#         self.firstUser1.save()
#         self.supervisor1 = Supervisor(user='firstUser', admin_dept='Engineering')
#         self.supervisor1.save()
#         self.course1 = Course(super_id='supervisor', course_name='Engineer 101', course_identifier='601', course_dept='Engineering', course_credits=3)
#         self.course1.save()
    
#     def testInitalValues(self):
#         self.assertEqual(self.course1.super_id, "supervisor")
#         self.assertEqual(self.course1.course_name, "Engineer 101")
#         self.assertEqual(self.course1.course_identifier, "601")
#         self.assertEqual(self.course1.course_dept, "Engineering")
#         self.assertEqual(self.course1.course_credits, 3)

#     def testModifyingValues(self):
#         self.course1.super_id = "new_id"
#         self.assertEqual(self.course1.super_id, "new_id")
#         self.course1.course_name = "Math Course"
#         self.assertEqual(self.course1.course_name, "Math Course")
#         self.course1.course_identifier = "101"
#         self.assertEqual(self.course1.course_identifier, "101")
#         self.course1.course_dept = "Mathematics"
#         self.assertEqual(self.course1.course_dept, "Mathematics")
#         self.course1.course_credits = 5
#         self.assertEqual(self.course1.course_credits, 5)