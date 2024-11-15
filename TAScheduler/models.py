from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

# Custom User Model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    fname = models.CharField(max_length=50, verbose_name="First Name")
    lname = models.CharField(max_length=50, verbose_name="Last Name")
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Phone Number")

    # Remove the username field
    username = None

    # Set email as the unique identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname', 'lname']

    objects = UserManager()  # Use the custom manager

    def __str__(self):
        return f"{self.fname} {self.lname}"

# Supervisor Model
class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name="supervisor_profile", null=True)
    admin_dept = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Supervisor"
        verbose_name_plural = "Supervisors"
        permissions = [
            ("create_courses", "Can create courses"),
            ("create_accounts", "Can create user accounts"),
            ("delete_accounts", "Can delete user accounts"),
            ("edit_accounts", "Can edit user accounts"),
            ("assign_instructors", "Can assign instructors to courses"),
            ("assign_tas", "Can assign TAs to courses and labs"),
            ("access_all_data", "Can access all system data"),
            ("send_notifications", "Can send notifications to users"),
        ]

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if this is a new instance
        super().save(*args, **kwargs)
        if is_new:  # Only assign permissions for new Supervisors
            content_type = ContentType.objects.get_for_model(Supervisor)
            permissions = Permission.objects.filter(content_type=content_type)
            self.user.user_permissions.add(*permissions)


    def __str__(self):
        return f"Supervisor: {self.user.fname} {self.user.lname} ({self.admin_dept})"


# # Instructor Model
# class Instructor(models.Model):
#     user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name="instructor_profile")
#     instructor_dept = models.CharField(max_length=100)

#     class Meta:
#         verbose_name = "Instructor"
#         verbose_name_plural = "Instructors"
#         permissions = [
#             ("edit_contact_info", "Can edit own contact information"),
#             ("view_course_assignments", "Can view course assignments"),
#             ("view_ta_assignments", "Can view TA assignments"),
#             ("assign_tas_to_labs", "Can assign TAs to specific lab sections"),
#             ("send_notifications", "Can send notifications to TAs"),
#             ("view_public_contact_info", "Can read public contact information of all users"),
#         ]

#     def save(self, *args, **kwargs):
#         is_new = self.pk is None  # Check if this is a new instance
#         super().save(*args, **kwargs)
#         if is_new:  # Only assign permissions for new Supervisors
#             content_type = ContentType.objects.get_for_model(Supervisor)
#             permissions = Permission.objects.filter(content_type=content_type)
#             self.user.user_permissions.add(*permissions)

#     def __str__(self):
#         return f"Instructor: {self.user.fname} {self.user.lname} ({self.instructor_dept})"


# #TA Model
# class TA(models.Model):
#     user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name="ta_profile")
#     ta_dept = models.CharField(max_length=100)

#     class Meta:
#         verbose_name = "TA"
#         verbose_name_plural = "TAs"
#         permissions = [
#             ("edit_contact_info", "Can edit own contact information"),
#             ("view_ta_assignments", "Can view TA assignments"),
#             ("view_public_contact_info", "Can read public contact information of all users"),
#         ]

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         content_type = ContentType.objects.get_for_model(TA)
#         permissions = Permission.objects.filter(content_type=content_type)
#         self.user.user_permissions.add(*permissions)

#     def __str__(self):
#         return f"TA: {self.user.fname} {self.user.lname} ({self.ta_dept})"



