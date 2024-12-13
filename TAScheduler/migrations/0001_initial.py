# Generated by Django 5.1.4 on 2024-12-13 07:02

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.AutoField(primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=100)),
                ('course_identifier', models.CharField(max_length=10)),
                ('course_dept', models.CharField(max_length=100)),
                ('course_credits', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instructor_dept', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Instructor',
                'verbose_name_plural': 'Instructors',
                'permissions': [('edit_contact_info', 'Can edit own contact information'), ('view_course_assignments', 'Can view course assignments'), ('view_ta_assignments', 'Can view TA assignments'), ('assign_tas_to_labs', 'Can assign TAs to specific lab sections'), ('send_notifications', 'Can send notifications to TAs'), ('view_public_contact_info', 'Can read public contact information of all users')],
            },
        ),
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_dept', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Supervisor',
                'verbose_name_plural': 'Supervisors',
                'permissions': [('create_courses', 'Can create courses'), ('create_accounts', 'Can create user accounts'), ('delete_accounts', 'Can delete user accounts'), ('edit_accounts', 'Can edit user accounts'), ('assign_instructors', 'Can assign instructors to courses'), ('assign_tas', 'Can assign TAs to courses and labs'), ('access_all_data', 'Can access all system data'), ('send_notifications', 'Can send notifications to users')],
            },
        ),
        migrations.CreateModel(
            name='TA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ta_dept', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'TA',
                'verbose_name_plural': 'TAs',
                'permissions': [('edit_contact_info', 'Can edit own contact information'), ('view_ta_assignments', 'Can view TA assignments'), ('view_public_contact_info', 'Can read public contact information of all users')],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('section_id', models.AutoField(primary_key=True, serialize=False)),
                ('section_num', models.IntegerField()),
                ('section_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Sections_course', to='TAScheduler.course')),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('lecture_id', models.AutoField(primary_key=True, serialize=False)),
                ('days_of_week', models.CharField(max_length=8)),
                ('lecture_startTime', models.DateTimeField()),
                ('lecture_endTime', models.DateTimeField()),
                ('lecture_instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Lecture_Instructor', to='TAScheduler.instructor')),
                ('lecture_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lecture_section', to='TAScheduler.section')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='super_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_supervisor', to='TAScheduler.supervisor'),
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('lab_id', models.AutoField(primary_key=True, serialize=False)),
                ('days_of_week', models.CharField(max_length=7)),
                ('lab_startTime', models.DateTimeField()),
                ('lab_endTime', models.DateTimeField()),
                ('lab_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lab_section', to='TAScheduler.section')),
                ('lab_ta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Lab_TA', to='TAScheduler.ta')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('fname', models.CharField(max_length=50, verbose_name='First Name')),
                ('lname', models.CharField(max_length=50, verbose_name='Last Name')),
                ('address', models.CharField(max_length=50)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, verbose_name='Phone Number')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='ta',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='email'),
        ),
        migrations.AddField(
            model_name='supervisor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='email'),
        ),
        migrations.AddField(
            model_name='instructor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='email'),
        ),
    ]
