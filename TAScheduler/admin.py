
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import *
from .forms import SupervisorAdminForm, UserForm

# Base User Admin
@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    add_form = UserForm  # Use your custom creation form
    list_display = ('email', 'fname', 'lname', 'is_staff', 'is_active')
    search_fields = ('email', 'fname', 'lname')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('fname', 'lname', 'phone_number', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fname', 'lname', 'phone_number', 'address', 'password1', 'password2'),
        }),
    )

# Supervisor Admin
@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    form = SupervisorAdminForm  # Custom form for Supervisor
    list_display = ('get_email', 'get_fname', 'get_lname', 'admin_dept')
    search_fields = ('user__email', 'user__fname', 'user__lname', 'admin_dept')

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_fname(self, obj):
        return obj.user.fname
    get_fname.short_description = 'First Name'

    def get_lname(self, obj):
        return obj.user.lname
    get_lname.short_description = 'Last Name'

# Instructor Admin
@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'get_fname', 'get_lname', 'instructor_dept')
    search_fields = ('user__email', 'user__fname', 'user__lname', 'instructor_dept')

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_fname(self, obj):
        return obj.user.fname
    get_fname.short_description = 'First Name'

    def get_lname(self, obj):
        return obj.user.lname
    get_lname.short_description = 'Last Name'

# TA Admin
@admin.register(TA)
class TAAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'get_fname', 'get_lname', 'ta_dept')
    search_fields = ('user__email', 'user__fname', 'user__lname', 'ta_dept')

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_fname(self, obj):
        return obj.user.fname
    get_fname.short_description = 'First Name'

    def get_lname(self, obj):
        return obj.user.lname
    get_lname.short_description = 'Last Name'

from django.contrib import admin
from .models import Lab, Section, Lecture, Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'course_identifier', 'course_dept', 'course_credits', 'super_id')
    search_fields = ('course_name', 'course_identifier', 'course_dept')
    list_filter = ('course_dept',)
    ordering = ('course_name',)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('section_num', 'section_course')
    search_fields = ('section_num', 'section_course__course_name')
    list_filter = ('section_course__course_dept',)
    ordering = ('section_num',)


@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ('lab_section', 'lab_ta', 'days_of_week', 'lab_startTime', 'lab_endTime')
    search_fields = ('lab_section__section_course__course_name', 'lab_ta__user__email')
    list_filter = ('days_of_week',)
    ordering = ('lab_startTime',)


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('lecture_section', 'lecture_instructor', 'days_of_week', 'lecture_startTime', 'lecture_endTime')
    search_fields = ('lecture_section__section_course__course_name', 'lecture_instructor__user__email')
    list_filter = ('days_of_week',)
    ordering = ('lecture_startTime',)

