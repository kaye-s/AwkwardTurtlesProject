from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from TAScheduler.utils.auth import group_required  # Import the group_required decorator
from TAScheduler.utils.account_management import create_user_account, edit_user_account, delete_user_account  # Utility functions


User = get_user_model()

@method_decorator([group_required('Supervisor'),  login_required], name='dispatch')
class AccountManagementView(View):
    """
    Handles account management tasks accessible only to Supervisors.
    """

    def get(self, request):
        """
        Renders the account management page with users who are not superusers.
        """
        users = User.objects.filter(is_superuser=False)  # Exclude superusers
        return render(request, 'AccountManagement.html', {'users': users})

    def post(self, request):
        """
        Handles account management actions: create, edit, or delete a user account.
        """
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