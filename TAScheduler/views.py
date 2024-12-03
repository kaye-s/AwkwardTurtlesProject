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
        return
    

@method_decorator([group_required('Supervisor'), login_required], name='dispatch')
class CourseView(View):
    """
    Handles course management tasks accessible only to Supervisors.
    """

    def get(self, request):
        """
        Renders the course management page with a list of all courses.
        """
        courses = Course.objects.all()  # Replace `Course` with your actual model name
        return render(request, 'CourseManagement.html', {'courses': courses})

    def post(self, request):
        """
        Handles course management actions: create, edit, or delete a course.
        """
        action = request.POST.get('action')

        if action == 'create':
            return create_course(request)
        elif action == 'edit':
            return edit_course(request)
        elif action == 'delete':
            return delete_course(request)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
