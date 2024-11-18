from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

def create_user_account(request):
    """
    Handles the creation of a new user account.
    """
    email = request.POST.get('email')
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    password = request.POST.get('password')

    if email and fname and lname and password:
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=fname,
            last_name=lname
        )
        user.save()
        messages.success(request, f"User {email} has been created.")
    else:
        messages.error(request, "Invalid data for creating user.")
    
    return redirect('account_management')


def edit_user_account(request):
    """
    Handles editing of an existing user account.
    """
    user_id = request.POST.get('user_id')
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')

    user = get_object_or_404(User, id=user_id)
    if fname:
        user.first_name = fname
    if lname:
        user.last_name = lname
    user.save()

    messages.success(request, f"User {user.email} has been updated.")
    return redirect('account_management')


def delete_user_account(request):
    """
    Handles deletion of an existing user account.
    """
    user_id = request.POST.get('user_id')
    user = get_object_or_404(User, id=user_id)
    user.delete()

    messages.success(request, f"User {user.email} has been deleted.")
    return redirect('account_management')