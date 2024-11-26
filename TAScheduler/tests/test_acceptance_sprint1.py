from django.test import TestCase
from django.contrib.auth.models import Permission
from TAScheduler.models import User, Supervisor

class SBICreateAccounts(TestCase):

    #Unsure exactly what is neeed yet
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

    # Test1
        # Supervisor successful login
        # Navigate to Account Management Page
        # Click on create user
        # Complete form
        # Email is unique
        # Submit
        # User is added to database

    # Test2
        # Supervisor successful login
        # Navigate to Account Management Page
        # Click on create user
        # Incomplete form
        # Displays error message

    # Test3
        # Supervisor successful login
        # Navigate to Account Management Page
        # Click on create user
        # Complete form
        # Email is NOT unique
        # Displays error message

    # Test4
        # TA successful login
        # Navigate to Account Management Page
        # Displays error message

    # Test5
        # Instructor successful login
        # Navigate to Account Management Page
        # Displays error message

class SBIEditAccounts(TestCase):

    #Unsure exactly what is needed yet
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

    # Test1
        # Supervisor successful login
        # Navigate to Account Management Page
        # Click on edit user
        # Form displays current information for the given user
        # Supervisor changes a field
        # Hits submit
        # Information is updated in the database

    # Test1
        # Supervisor successful login
        # Navigate to Account Management Page
        # Click on edit user
        # Form displays current information for the given user
        # Supervisor changes a field
        # Hits submit
        # Information is updated in the database