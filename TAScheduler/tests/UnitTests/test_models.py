from django.test import TestCase
from django.contrib.auth.models import Permission
from TAScheduler.models import User, TA, Instructor, Supervisor, Course, Section, Lab, Lecture

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
        self.firstUser1 = User(email="supervisor@example.com", password="blank123", fname="John", lname="Doe", address='1234 Oaklane Rd', phone_number='123-456-7890')
        self.firstUser1.save()
        self.supervisor1 = Supervisor(user=self.firstUser1, admin_dept='Engineering')
        self.supervisor1.save()
        self.course1 = Course(super_id=self.supervisor1, course_name='Engineer 101', course_identifier='601', course_dept='Engineering', course_credits=3)
        self.course1.save()

    def testAccessThoughFK(self):
        course1sup = self.course1.super_id
        sup1user = course1sup.user
        self.assertEqual(sup1user, self.firstUser1)

    def testModifyingValues(self):
        self.firstUser1.fname = "Sally"
        self.assertEqual(self.firstUser1.fname, "Sally")

class CourseTests(TestCase):
    def setUp(self):
        self.firstUser1 = User(email="supervisor@example.com", password="blank123", fname="John", lname="Doe", address='1234 Oaklane Rd', phone_number='123-456-7890')
        self.secondUser1 = User(email="ta@example.com", password="blank123", fname="Richard", lname="Smith",
                                address='5555 Wood Lane', phone_number='999-888-1234')
        self.firstUser1.save()
        self.secondUser1.save()
        self.supervisor1 = Supervisor(user=self.firstUser1, admin_dept='Engineering')
        self.supervisor1.save()
        self.course1 = Course(super_id=self.supervisor1, course_name='Engineer 101', course_identifier='601', course_dept='Engineering', course_credits=3)
        self.course1.save()

    def testInitialValueSuperId(self):
        self.assertEqual(self.course1.super_id, self.supervisor1)

    def testInitialValueCourseName(self):
        self.assertEqual(self.course1.course_name, "Engineer 101")

    def testInitialValueCourseIdentifier(self):
        self.assertEqual(self.course1.course_identifier, "601")

    def testInitialValueCourseDept(self):
        self.assertEqual(self.course1.course_dept, "Engineering")

    def testInitialValueCourseCredits(self):
        self.assertEqual(self.course1.course_credits, 3)

    def testModifyValueSuperId(self):
        newSupervisor = Supervisor(user=self.secondUser1, admin_dept='Tech')
        newSupervisor.save()
        self.course1.super_id = newSupervisor
        self.assertEqual(self.course1.super_id, newSupervisor)

    def testModifyValueCourseName(self):
        self.course1.course_name = "New Course name"
        self.assertEqual(self.course1.course_name, "New Course name")

    def testModifyValueCourseIdentifier(self):
        self.course1.course_identifier = "333"
        self.assertEqual(self.course1.course_identifier, "333")

    def testModifyValueCourseDept(self):
        self.course1.course_dept = "Flutes"
        self.assertEqual(self.course1.course_dept, "Flutes")

    def testModifyValueCourseCredits(self):
        self.course1.course_credits = 9
        self.assertEqual(self.course1.course_credits, 9)

class SectionTests(TestCase):
    def setUp(self):
        self.firstUser1 = User(email="supervisor@example.com", password="blank123", fname="John", lname="Doe", address='1234 Oaklane Rd', phone_number='123-456-7890')
        self.firstUser1.save()
        self.supervisor1 = Supervisor(user=self.firstUser1, admin_dept='Engineering')
        self.supervisor1.save()
        self.course1 = Course(super_id=self.supervisor1, course_name='Engineer 101', course_identifier='601', course_dept='Engineering', course_credits=3)
        self.course1.save()
        self.section1 = Section(section_num=303, section_course=self.course1)

    def testSectionInitialNum(self):
        self.assertEqual(self.section1.section_num, 303)

    def testSectionModifyNum(self):
        self.section1.section_num = 101
        self.assertEqual(self.section1.section_num, 101)

    def testSectionInitialCourse(self):
        self.assertEqual(self.section1.section_course, self.course1)

    def testSectionModifyCourse(self):
        newCourse = Course(super_id=self.supervisor1, course_name='Maths Course', course_identifier="1001", course_dept="Maths", course_credits=2)
        newCourse.save()
        self.section1.section_course = newCourse
        self.assertEqual(self.section1.section_course, newCourse)

class LabTests(TestCase):
    def setUp(self):
        self.firstUser1 = User(email="supervisor@example.com", password="blank123", fname="John", lname="Doe",
                               address='1234 Oaklane Rd', phone_number='123-456-7890')
        self.secondUser1 = User(email="ta@example.com", password="blank123", fname="Richard", lname="Smith",
                               address='5555 Wood Lane', phone_number='999-888-1234')
        self.firstUser1.save()
        self.secondUser1.save()
        self.supervisor1 = Supervisor(user=self.firstUser1, admin_dept='Engineering')
        self.supervisor1.save()
        self.course1 = Course(super_id=self.supervisor1, course_name='Engineer 101', course_identifier='601',
                              course_dept='Engineering', course_credits=3)
        self.course1.save()
        self.section1 = Section(section_num=303, section_course=self.course1)
        self.ta1 = TA(user=self.secondUser1, ta_dept="Arts")
        self.ta1.save()
        self.lab1 = Lab(lab_section=self.section1, lab_ta=self.ta1, days_of_week="MWF")

    def testInitialLabSection(self):
        self.assertEqual(self.lab1.lab_section, self.section1)

    def testModifyLabSection(self):
        newSection = Section(section_num=677, section_course=self.course1)
        newSection.save()
        self.lab1.lab_section = newSection
        self.assertEqual(self.lab1.lab_section, newSection)

    def testInitialTASection(self):
        self.assertEqual(self.lab1.lab_ta, self.ta1)

    def testModifyTASection(self):
        newTA = TA(user=self.firstUser1, ta_dept="Math")
        newTA.save()
        self.lab1.lab_ta = newTA
        self.assertEqual(self.lab1.lab_ta, newTA)

    def testInitialDOWSection(self):
        self.assertEqual(self.lab1.days_of_week, "MWF")

    def testModifyDOWSection(self):
        self.lab1.days_of_week = "TR"
        self.assertEqual(self.lab1.days_of_week, "TR")

class LectureTests(TestCase):
    def setUp(self):
        self.firstUser1 = User(email="supervisor@example.com", password="blank123", fname="John", lname="Doe",
                               address='1234 Oaklane Rd', phone_number='123-456-7890')
        self.secondUser1 = User(email="instructor@example.com", password="blank123", fname="Leah", lname="Smith",
                                address='6666 Pine Lane', phone_number='333-777-1234')
        self.firstUser1.save()
        self.secondUser1.save()
        self.instructor1 = Instructor(user= self.secondUser1, instructor_dept="Music")
        self.instructor1.save()
        self.supervisor1 = Supervisor(user=self.firstUser1, admin_dept='Engineering')
        self.supervisor1.save()
        self.course1 = Course(super_id=self.supervisor1, course_name='Engineer 101', course_identifier='601',
                              course_dept='Engineering', course_credits=3)
        self.course1.save()
        self.section1 = Section(section_num=303, section_course=self.course1)
        self.lecture1 = Lecture(lecture_section=self.section1,lecture_instructor=self.instructor1, days_of_week="WF")

    def testInitialLectureSection(self):
        self.assertEqual(self.lecture1.lecture_section, self.section1)

    def testModifyLectureSection(self):
        newSection = Section(section_num=677, section_course=self.course1)
        newSection.save()
        self.lecture1.lecture_section = newSection
        self.assertEqual(self.lecture1.lecture_section, newSection)

    def testInitialInstructorSection(self):
        self.assertEqual(self.lecture1.lecture_instructor, self.instructor1)

    def testModifyInstructorSection(self):
        newInstructor = Instructor(user=self.firstUser1, instructor_dept="Math")
        newInstructor.save()
        self.lecture1.lecture_instructor = newInstructor
        self.assertEqual(self.lecture1.lecture_instructor, newInstructor)

    def testInitialDOWSection(self):
        self.assertEqual(self.lecture1.days_of_week, "WF")

    def testModifyDOWSection(self):
        self.lecture1.days_of_week = "TR"
        self.assertEqual(self.lecture1.days_of_week, "TR")
        