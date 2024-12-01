from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from TAScheduler.models import *
from django.utils.html import escape

def create_user_account(request):
    """
    Handles the creation of a new user account.
    """
    email = escape(request.POST.get('email'))
    fname = escape(request.POST.get('fname'))
    lname = escape(request.POST.get('lname'))
    role = escape(request.POST.get('role'))
    dept = escape(request.POST.get('dept'))
    phone_number = escape(request.POST.get("phone_number"))
    address1=escape(request.POST.get("address1"))
    address2=escape(request.POST.get("address2"))
    password = escape(request.POST.get('password'))


    if email != 'None' and password != 'None':
        user = User.objects.create_user(
            email=email,
            password=password,
            fname=fname,
            lname=lname,
            address=address1+address2,
            phone_number=phone_number
        )
        user.save()
        obj = None
        if(role == "Supervisor"):
            obj = Supervisor(user=user, admin_dept=dept)
        elif(role == "TA"):
            obj = TA(user=user, ta_dept=dept)
        elif(role =="Instructor"):
            obj = Instructor(user=user, instructor_dept=dept)
        else:
            pass

        try:
            obj.save()
        except:
            pass #Shouldn't fail if role is not defined, but could be changed later
    elif email == 'None':
        messages.error(request, "Email cannot be empty") #Pass a message if the email is empty
    
    return redirect('account-management')


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
    return redirect('account-management')