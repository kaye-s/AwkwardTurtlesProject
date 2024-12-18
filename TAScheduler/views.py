from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from TAScheduler.utils.auth import group_required, method_group_required  # Import the group_required decorators
from TAScheduler.utils.account_management import create_user_account, edit_user_account, delete_user_account  # Utility functions
from TAScheduler.models import Supervisor, TA, Instructor
from TAScheduler.models import Course
from django.contrib import messages
from django.db import IntegrityError

User = get_user_model()

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Login page template
    redirect_authenticated_user = True  # Redirect if already logged in

    # Redirect all users to a single page after login
    def get_success_url(self):
        return reverse_lazy('account-management') 



#Handles account management tasks accessible only to Supervisors.
@method_decorator([login_required(login_url="/")], name='dispatch')
class AccountManagementView(View):
   
    #Renders the account management page with users who are not superusers.
    def get(self, request):
        s,i,t,alr = Supervisor.objects.all(), Instructor.objects.all(), TA.objects.all(), User.objects.all().order_by("-date_joined")[:4]
        if(request.user.groups.all().exists()):
            role = str(request.user.groups.all()[0])
        else:
            role = "Supervisor" #Workaround
        return render(request, 'AccountManagement.html', {'supervisors': s, "tas":t, "instructors":i, "role":role, "allUsers":alr})
    
    #Handles account management actions: create, edit, or delete a user account.
    @method_group_required("Supervisor")
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

class Login(View):
    def get(self,request):
        return render(request, "login.html", {})

    # POST REQUEST FOR ACCOUNT MANAGEMENT FORM
    def post(self, request):

        #something like this from parking lab to handle data
        # sec = request.POST.get('section')
        # date = request.POST.get('dateTime')

        # fill in context to handle database data

       return render(request, "login.html", {})

@login_required
@group_required('Supervisor')
def courses_supervisor(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        # Handle Create, Edit, and Delete based on action
        if action == 'create':
            return create_course(request)
        elif action == 'edit':
            course_id = request.POST.get('course_id')
            return edit_course(request, course_id)
        elif action == 'delete':
            course_id = request.POST.get('course_id')
            return delete_course(request, course_id)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
    else:
        # Display all courses for GET requests
        courses = Course.objects.all()
        return render(request, 'courses_supervisor.html', {'courses': courses, 'role':'Supervisor'})


# Create a new course
@login_required
@group_required('Supervisor')
def create_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course_identifier = request.POST.get('course_identifier')
        course_dept = request.POST.get('course_dept')
        course_credits = request.POST.get('course_credits')

        # Check if a course with the same identifier already exists
        if Course.objects.filter(course_identifier=course_identifier).exists():
            messages.error(request, f"A course with the identifier '{course_identifier}' already exists.")
            return redirect('courses-supervisor')

        # Create the course if no duplicate is found
        try:
            Course.objects.create(
                course_name=course_name,
                course_identifier=course_identifier,
                course_dept=course_dept,
                course_credits=course_credits,
                super_id=request.user.supervisor
            )
            messages.success(request, "Course created successfully.")
        except IntegrityError:
            messages.error(request, "An error occurred while creating the course.")

        return redirect('courses-supervisor')

# Edit an existing course
@login_required
@group_required('Supervisor')
def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        course.course_name = request.POST.get('course_name')
        course.course_identifier = request.POST.get('course_identifier')
        course.course_dept = request.POST.get('course_dept')
        course.course_credits = request.POST.get('course_credits')
        course.save()
        return redirect('courses-supervisor')


# Delete a course
@login_required
@group_required('Supervisor')
def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('courses-supervisor')
    return redirect('courses-supervisor')