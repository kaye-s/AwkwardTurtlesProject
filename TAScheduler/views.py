from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from TAScheduler.utils.auth import group_required  # Import the group_required decorator
from TAScheduler.utils.account_management import create_user_account, edit_user_account, delete_user_account  # Utility functions
from TAScheduler.models import Supervisor, TA, Instructor


User = get_user_model()

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Login page template
    redirect_authenticated_user = True  # Redirect if already logged in

    # Redirect all users to a single page after login
    def get_success_url(self):
        return reverse_lazy('account-management') 



#Handles account management tasks accessible only to Supervisors.
@method_decorator([login_required(login_url="/"), group_required('Supervisor')], name='dispatch')
class AccountManagementView(View):
   
    #Renders the account management page with users who are not superusers.
    def get(self, request):
        s,i,t = Supervisor.objects.all(), Instructor.objects.all(), TA.objects.all()
        return render(request, 'AccountManagement.html', {'supervisors': s, "tas":t, "instructors":i, "role":"Supervisor"})
    
    #Handles account management actions: create, edit, or delete a user account.
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

