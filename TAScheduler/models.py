from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission,Group

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
        return f"{self.email}"

# Supervisor Model
class Supervisor(models.Model):
    user = models.OneToOneField(User, to_field="email", on_delete=models.CASCADE)
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
        if is_new and self.user:
            # Define the group name
            group_name = 'Supervisor'

            # Get or create the group
            group, created = Group.objects.get_or_create(name=group_name)

            if created:
                # If the group was created, assign all Supervisor permissions to it
                content_type = ContentType.objects.get_for_model(Supervisor)
                permissions = Permission.objects.filter(content_type=content_type)
                group.permissions.set(permissions)
                group.save()

            # Add the user to the group
            self.user.groups.add(group)
            self.user.save()

    def __str__(self):
        return f"Supervisor: {self.user.fname} {self.user.lname} of ({self.admin_dept})"

# Instructor Model
class Instructor(models.Model):
    user = models.ForeignKey(User, to_field='email',on_delete=models.CASCADE)
    instructor_dept = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Instructor"
        verbose_name_plural = "Instructors"
        permissions = [
            ("edit_contact_info", "Can edit own contact information"),
            ("view_course_assignments", "Can view course assignments"),
            ("view_ta_assignments", "Can view TA assignments"),
            ("assign_tas_to_labs", "Can assign TAs to specific lab sections"),
            ("send_notifications", "Can send notifications to TAs"),
            ("view_public_contact_info", "Can read public contact information of all users"),
        ]

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if this is a new instance
        super().save(*args, **kwargs)
        if is_new and self.user:
            # Define the group name
            group_name = 'Instructor'

            # Get or create the group
            group, created = Group.objects.get_or_create(name=group_name)

            if created:
                # If the group was created, assign all Supervisor permissions to it
                content_type = ContentType.objects.get_for_model(Instructor)
                permissions = Permission.objects.filter(content_type=content_type)
                group.permissions.set(permissions)
                group.save()

            # Add the user to the group
            self.user.groups.add(group)
            self.user.save()


    def __str__(self):
        return f"Instructor: {self.user.fname} {self.user.lname} of ({self.instructor_dept})"


#TA Model
class TA(models.Model):
    user = models.ForeignKey(User, to_field='email',on_delete=models.CASCADE)
    ta_dept = models.CharField(max_length=100)

    class Meta:
        verbose_name = "TA"
        verbose_name_plural = "TAs"
        permissions = [
            ("edit_contact_info", "Can edit own contact information"),
            ("view_ta_assignments", "Can view TA assignments"),
            ("view_public_contact_info", "Can read public contact information of all users"),
        ]

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if this is a new instance
        super().save(*args, **kwargs)
        if is_new and self.user:
            # Define the group name
            group_name = 'TA'

            # Get or create the group
            group, created = Group.objects.get_or_create(name=group_name)

            if created:
                # If the group was created, assign all Supervisor permissions to it
                content_type = ContentType.objects.get_for_model(TA)
                permissions = Permission.objects.filter(content_type=content_type)
                group.permissions.set(permissions)
                group.save()

            # Add the user to the group
            self.user.groups.add(group)
            self.user.save()

    def __str__(self):
        return f"TA: {self.user.fname} {self.user.lname} of ({self.ta_dept})"

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    super_id = models.ForeignKey(Supervisor, to_field='id',on_delete=models.CASCADE, related_name='course_supervisor')
    course_name = models.CharField(max_length=100)
    course_identifier = models.CharField(max_length=10, unique=True)
    course_dept = models.CharField(max_length=100)
    course_credits = models.IntegerField()
    course_ta = models.ManyToManyField(TA)
    # User Course.course_ta.add(*TA OBJECT*) in order to add a TA to the course
    # *COURSE OBJECT*.course_ta.all() to get a queryset of all TAs in the course
    # Course.objects.filter(course_ta=*TA OBJECT*) to see all courses a ta is in
    course_instructor = models.ForeignKey(Instructor, to_field='id', on_delete=models.CASCADE, related_name="Course_Instructor", null=True, blank=True)

class Section(models.Model):
    section_id = models.AutoField(primary_key=True)
    section_type = models.CharField(max_length=15, blank=False)
    section_num = models.IntegerField()
    section_course = models.ForeignKey(Course, to_field='course_id', on_delete=models.CASCADE, related_name="Sections_course")
    days_of_week = models.CharField(max_length=7)
    section_startTime = models.TimeField(auto_now=False, auto_now_add=False)
    section_endTime = models.TimeField(auto_now=False, auto_now_add=False)
    section_ta = models.ForeignKey(TA, to_field='id', on_delete=models.CASCADE, related_name="Section_TA", null=True, blank=True)
    lecture_instructor = models.ForeignKey(Instructor, to_field='id', on_delete=models.CASCADE, related_name="Lecture_Instructor", null=True, blank=True)
