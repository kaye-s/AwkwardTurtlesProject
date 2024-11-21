
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User, Supervisor  # Uncomment Instructor and TA when ready
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


# Uncomment these when ready
# # Instructor Admin
# @admin.register(Instructor)
# class InstructorAdmin(admin.ModelAdmin):
#     list_display = ('get_email', 'get_fname', 'get_lname', 'instructor_dept')
#     search_fields = ('user__email', 'user__fname', 'user__lname', 'instructor_dept')

# # TA Admin
# @admin.register(TA)
# class TAAdmin(admin.ModelAdmin):
#     list_display = ('get_email', 'get_fname', 'get_lname', 'ta_dept')
#     search_fields = ('user__email', 'user__fname', 'user__lname', 'ta_dept')

