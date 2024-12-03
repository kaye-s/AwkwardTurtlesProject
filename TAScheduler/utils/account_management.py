from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from TAScheduler.models import *
from django.utils.html import escape

def populate_dict(request):
    return {
        'email' : escape(request.POST.get('email')),
        'fname' : escape(request.POST.get('fname')),
        'lname' : escape(request.POST.get('lname')),
        'role' : escape(request.POST.get('role')),
        'dept' : escape(request.POST.get('dept')),
        'phone_number' : escape(request.POST.get("phone_number")),
        'address1' : escape(request.POST.get("address1")),
        'address2' : escape(request.POST.get("address2")),
        'password' : escape(request.POST.get('password'))
    }


def create_user_account(request):
    """
    Handles the creation of a new user account.
    """
    context = populate_dict(request)
    passes_constraint = not User.objects.filter(email=context['email']).exists() #checks if the sent email is unique

    if passes_constraint and context['email'] != 'None' and context['password'] != 'None':
        user = User.objects.create_user(
            email=context['email'],
            password=context['password'],
            fname=context['fname'],
            lname=context['lname'],
            address=context['address1']+"<TASCheduler_delimiter>"+context['address2'],
            phone_number=context['phone_number']
        )
        user.save()
        obj = None
        if(context['role'] == "Supervisor"):
            obj = Supervisor(user=user, admin_dept=context['dept'])
        elif(context['role'] == "TA"):
            obj = TA(user=user, ta_dept=context['dept'])
        elif(context['role'] =="Instructor"):
            obj = Instructor(user=user, instructor_dept=context['dept'])
        else:
            pass
        try:
            obj.save()
        except:
            pass #Shouldn't fail if role is not defined, but could be changed later

    elif context['email'] == 'None':
        messages.error(request, "Email cannot be empty") #Pass a message if the email is empty
    elif context['password'] == 'None':
        messages.error(request, "Must create a password") #Pass a message if the email is empty
    
    elif not passes_constraint:
        messages.error(request, "Email already exists in the system") #Now passes a message if the email isn't unique
    
    return redirect('account-management')


def edit_user_account(request):
    """
    Handles editing of an existing user account.
    """
    user_role = request.POST.get('old_role')
    user_id = request.POST.get('user_id')
    did_change = False

    # Fetching form data
    context = populate_dict(request)

    # Fetch role-specific object
    obj = None
    if user_role == "Supervisor":
        obj = get_object_or_404(Supervisor, user_id=user_id)
    elif user_role == "Instructor":
        obj = get_object_or_404(Instructor, user_id=user_id)
    elif user_role == "TA":
        obj = get_object_or_404(TA, user_id=user_id)

    if obj is not None:
        user = obj.user  # Access the related user object

        # Update User fields
        if context['fname'] != 'None' and user.first_name != context['fname']:
            did_change = True
            user.fname = context['fname']
        if context['lname'] != 'None' and user.last_name != context['lname']:
            did_change = True
            user.lname = context['lname']
        if context['phone_number'] != 'None' and user.phone_number != context['phone_number']:
            did_change = True
            user.phone_number = context['phone_number']  # Assuming phone_number exists in your custom user model
        if context['address1'] != 'None':
            new_address = context['address1'] + "<TASCheduler_delimiter>" + context['address2']
            if user.address != new_address:
                did_change = True
                user.address = new_address

        # Update Password
        if context['password'] != 'None' and not check_password(context['password'], user.password):
            did_change = True
            user.password = make_password(context['password'])

        # Save User changes
        if did_change:
            user.save()

        # Update role-specific fields
        if user_role == context['role']:  # Same role, update department only
            if user_role == "Supervisor" and obj.admin_dept != context['dept']:
                obj.admin_dept = context['dept']
                obj.save()
            elif user_role == "Instructor" and obj.instructor_dept != context['dept']:
                obj.instructor_dept = context['dept']
                obj.save()
            elif user_role == "TA" and obj.ta_dept != context['dept']:
                obj.ta_dept = context['dept']
                obj.save()
        else:
            obj.delete()  # Delete the current role-specific object
            if context['role'] == "Supervisor":
                Supervisor.objects.create(user=user, admin_dept=context['dept'])
            elif context['role'] == "Instructor":
                Instructor.objects.create(user=user, instructor_dept=context['dept'])
            elif context['role'] == "TA":
                TA.objects.create(user=user, ta_dept=context['dept'])

    return redirect('account-management')


def delete_user_account(request):
    """
    Handles deletion of an existing user account.
    """
    user_id = request.POST.get('user_id')
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('account-management')