from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
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


    if email and fname and lname and role and password and address1 and dept:
        user = User.objects.create_user(
            email=email,
            password=password,
            fname=fname,
            lname=lname,
            address=address1+"<TASCheduler_delimiter>"+address2,
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
        obj.save()
    
    return redirect('account-management')


def edit_user_account(request):
    """
    Handles editing of an existing user account.
    """
    user_role = request.POST.get('old_role')
    user_id = request.POST.get('user_id')
    did_change = False

    # Fetching form data
    fname = escape(request.POST.get('fname'))
    lname = escape(request.POST.get('lname'))
    email = escape(request.POST.get('email'))
    role = escape(request.POST.get('role'))
    dept = escape(request.POST.get('dept'))
    phone_number = escape(request.POST.get("phone_number"))
    address1 = escape(request.POST.get("address1"))
    address2 = escape(request.POST.get("address2"))
    password = escape(request.POST.get('password'))

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
        if fname and user.first_name != fname:
            did_change = True
            print("here is a debug")
            user.fname = fname
        if lname and user.last_name != lname:
            did_change = True
            user.lname = lname
        if email and user.email != email:
            did_change = True
            user.email = email
        if phone_number and user.phone_number != phone_number:
            did_change = True
            user.phone_number = phone_number  # Assuming phone_number exists in your custom user model
        if address1 or address2:
            new_address = address1 + "<TASCheduler_delimiter>" + address2
            if user.address != new_address:
                did_change = True
                user.address = new_address

        # Update Password
        if password and not check_password(password, user.password):
            did_change = True
            user.password = make_password(password)

        # Save User changes
        if did_change:
            user.save()

        # Update role-specific fields
        if user_role == role:  # Same role, update department only
            if user_role == "Supervisor" and obj.admin_dept != dept:
                obj.admin_dept = dept
                obj.save()
            elif user_role == "Instructor" and obj.instructor_dept != dept:
                obj.instructor_dept = dept
                obj.save()
            elif user_role == "TA" and obj.ta_dept != dept:
                obj.ta_dept = dept
                obj.save()
        else:
            obj.delete()  # Delete the current role-specific object
            if role == "Supervisor":
                Supervisor.objects.create(user=user, admin_dept=dept)
            elif role == "Instructor":
                Instructor.objects.create(user=user, instructor_dept=dept)
            elif role == "TA":
                TA.objects.create(user=user, ta_dept=dept)

    return redirect('account-management')


def delete_user_account(request):
    """
    Handles deletion of an existing user account.
    """
    user_id = request.POST.get('user_id')
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('account-management')