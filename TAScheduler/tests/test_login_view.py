from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import Permission
from TAScheduler.models import User, Supervisor


class LoginTest(TestCase):
    monkey = None
    thingList = None

    def setUp(self):
        self.monkey = Client()
        firstUser = User(email="supervisor@example.com", password="blank123", fname="John", lname="Doe",
                         address='1234 Oaklane Rd', phone_number='123-456-7890')
        secondUser = User(email="supervisor2@example.com", password="blank456", fname="Jane", lname="Smith",
                         address='1234 Oaklane Rd', phone_number='123-456-7890')
        supervisor = Supervisor()

    def test_noPassword(self):
        r = self.monkey.post("/", {"email": "supervisor@example.com", "password": ""}, follow=True)
        self.assertEqual(r.context["message"], "bad password", "Blank password field should print error message")

    def test_badPassword(self):
        r = self.monkey.post("/", {"email": "supervisor@example.com", "password": "password"}, follow=True)
        self.assertEqual(r.context["message"], "bad password", "Incorrect password should print error message")

    def test_mismatchPassword(self):
        r = self.monkey.post("/", {"email": "supervisor@example.com", "password": "blank456"}, follow=True)
        self.assertEqual(r.context["message"], "bad password",
                         "Using the password of another user should print error message")

    def test_correctPassword(self):
        r = self.monkey.post("/", {"email": "supervisor@example.com", "password": "blank123"}, follow=True)
        self.assertEqual(r.context["message"], "valid password",
                         "Correct Password")