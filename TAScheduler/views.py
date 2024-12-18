from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from TAScheduler.utils.auth import group_required  # Import the group_required decorator
from TAScheduler.utils.account_management import create_user_account, edit_user_account, \
    delete_user_account  # Utility functions
from TAScheduler.utils.courses import create_course, edit_course, delete_course, assignTA_course, removeTA_course, create_section, delete_section, edit_section
from TAScheduler.models import Supervisor, TA, Instructor
from TAScheduler.models import Course, Section
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q
#
User = get_user_model()


class CustomLoginView(LoginView):
    template_name = 'login.html'  # Login page template
    redirect_authenticated_user = True  # Redirect if already logged in

    # Redirect all users to a single page after login
    def get_success_url(self):
        return reverse_lazy('account-management')

    # Handles account management tasks accessible only to Supervisors.


@method_decorator([login_required(login_url="/"), group_required('Supervisor')], name='dispatch')
class AccountManagementView(View):

    # Renders the account management page with users who are not superusers.
    def get(self, request):
        s, i, t = Supervisor.objects.all(), Instructor.objects.all(), TA.objects.all()
        return render(request, 'AccountManagement.html',
                      {'supervisors': s, "tas": t, "instructors": i, "role": "Supervisor"})

    # Handles account management actions: create, edit, or delete a user account.
    def post(self, request):
        action = request.POST.get('action')

        if action == 'create':
            return create_user_account(request)
        elif action == 'edit':
            return edit_user_account(request)
        elif action == 'delete':
            return delete_user_account(request)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

@method_decorator([login_required(login_url="/"), group_required('Supervisor')], name='dispatch')
class Courses_Supervisor(View):
    def get(self, request):
        courses = Course.objects.all()
        tas = TA.objects.all()
        instructors = Instructor.objects.all()
        return render(request, 'courses_supervisor.html',
                      {'courses': courses, 'instructors': instructors, 'tas': tas, 'role': 'Supervisor'})

    def post(self, request):
        action = request.POST.get('action')

        # Handle Create, Edit, and Delete based on action
        if action == 'createCourse':
            return create_course(request)
        elif action == 'editCourse':
            course_id = request.POST.get('course_id')
            return edit_course(request, course_id)
        elif action == 'deleteCourse':
            course_id = request.POST.get('course_id')
            return delete_course(request, course_id)
        elif action == 'addTACourse':
            course_id = request.POST.get('course_id')
            return assignTA_course(request, course_id)
        elif action == 'deleteTACourse':
            course_id = request.POST.get('course_id')
            return removeTA_course(request, course_id)
        elif action == 'createSection':
            return create_section(request)
        elif action == 'editSection':
            section_id = request.POST.get('section_id')
            return edit_section(request, section_id)
        elif action == 'deleteSection':
            section_id = request.POST.get('section_id')
            return delete_section(request, section_id)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)




# @login_required
# @group_required('Supervisor')
# def sections_supervisor(request):
#     if request.method == 'POST':
#         action = request.POST.get('action')
#
#         # Handle Create, Edit, and Delete based on action
#         if action == 'create':
#             return create_section(request)
#         elif action == 'edit':
#             section_id = request.POST.get('section_id')
#             return edit_section(request, section_id)
#         elif action == 'delete':
#             section_id = request.POST.get('section_id')
#             return delete_course(request, section_id)
#         else:
#             return JsonResponse({'error': 'Invalid action'}, status=400)
#     else:
#         # Display all courses for GET requests
#         sections = Section.objects.all()
#         instructors = Instructor.objects.all()
#         return render(request, 'courses_supervisor.html',
#                       {'sections': sections, 'instructors': instructors, 'role': 'Supervisor'})


# Create a new course
# @login_required
# @group_required('Supervisor')
# def create_section(request):
#     instructors = Instructor.objects.all()
#     # retrieve all instructors
#
#     if request.method == 'POST':
#         section_name = request.POST.get('section_name')
#         section_identifier = request.POST.get('section_identifier')
#         section_dept = request.POST.get('section_dept')
#         section_credits = request.POST.get('section_credits')
#         instructor_id = request.POST.get('instructor_id')
#
#         instructor = Instructor.objects.filter(id=instructor_id).first()
#
#         # Check if a course with the same identifier already exists
#         if Section.objects.filter(course_identifier=section_identifier).exists():
#             messages.error(request, f"A section with the identifier '{section_identifier}' already exists.")
#             return redirect('courses-supervisor')
#
#         # Create the course if no duplicate is found
#         try:
#             Section.objects.create(
#                 section_name=section_name,
#                 section_identifier=section_identifier,
#                 section_dept=section_dept,
#                 section_credits=section_credits,
#                 instructor=instructor,
#                 super_id=request.user.supervisor
#             )
#             messages.success(request, "Section created successfully.")
#         except IntegrityError:
#             messages.error(request, "An error occurred while creating the section.")
#
#         return redirect('courses-supervisor')
#
#
# # Edit an existing course
# @login_required
# @group_required('Supervisor')
# def edit_section(request, section_id):
#     section = get_object_or_404(Course, pk=section_id)
#     instructors = Instructor.objects.all()
#
#     if request.method == 'POST':
#         section.course_name = request.POST.get('section_name')
#         section.course_identifier = request.POST.get('section_identifier')
#         section.course_dept = request.POST.get('section_dept')
#         section.course_credits = request.POST.get('section_credits')
#         instructor_id = request.POST.get('instructor_id')
#
#         instructor = Instructor.objects.filter(id=instructor_id).first()
#         section.instructor = instructor
#
#         section.save()
#         return redirect('courses-supervisor')
#
#
# # Delete a course
# @login_required
# @group_required('Supervisor')
# def delete_section(request, section_id):
#     section = get_object_or_404(Course, pk=section_id)
#     if request.method == 'POST':
#         section.delete()
#         return redirect('courses-supervisor')
#     return redirect('courses-supervisor')

#this is my commit ahhhh
class courses_other(View):
    def get(self, request):
        courses = Course.objects.all()

        instructors = Instructor.objects.all()
        return render(request, 'courses_other.html',
                  {'courses': courses, 'instructors': instructors, 'role': 'Supervisor'})

class AccountOtherView(View):

    # Renders the account management page with users who are not superusers.
    def get(self, request):
        s, i, t = Supervisor.objects.all(), Instructor.objects.all(), TA.objects.all()
        return render(request, 'Account_other.html',
                      {'supervisors': s, "tas": t, "instructors": i, "role": "Supervisor"})


class ContactInfoView(View):
    def get(self, request):
        current_user = request.user
        search_query = request.GET.get('search', '').strip()

        def search_users(model):
            if ' ' in search_query:
                first_name, last_name = search_query.split(' ', 1)
                return model.objects.filter(
                    Q(user__fname__icontains=first_name) &
                    Q(user__lname__icontains=last_name)
                )
            else:
                return model.objects.filter(
                    Q(user__fname__icontains=search_query) |
                    Q(user__lname__icontains=search_query) |
                    Q(user__email__icontains=search_query)
                )

        supervisors = search_users(Supervisor)
        instructors = search_users(Instructor)
        tas = search_users(TA)

        return render(request, 'contact_info_page.html', {
            'current_user': current_user,
            'supervisors': supervisors,
            'instructors': instructors,
            'tas': tas,
            'search_query': search_query,
        })

    def post(self, request):
        # Allow users to update their contact information
        user = request.user
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')

        # Update only the fields provided
        if fname:
            user.fname = fname
        if lname:
            user.lname = lname
        if email:
            user.email = email
        if address:
            user.address = address
        if phone_number:
            user.phone_number = phone_number

        user.save()

        messages.success(request, "Your contact information has been updated.")
        return redirect('contact-info')  # Adjust the URL name to match your project
