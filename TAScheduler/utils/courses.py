from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from TAScheduler.models import *
from django.utils.html import escape
from django.db import IntegrityError

def populate_dict(request):
    return {
        'course_id' : escape(request.POST.get('course_id')),
        'super_id' : escape(request.POST.get('super_id')),
        'course_name' : escape(request.POST.get('course_name')),
        'course_identifier' : escape(request.POST.get('course_identifier')),
        'course_dept' : escape(request.POST.get('course_dept')),
        'course_credits' : escape(request.POST.get("course_credits")),
        'course_ta' : escape(request.POST.get("course_ta")),
        'instructor' : escape(request.POST.get("instructor")),

    }


def create_course(request):
    instructors = Instructor.objects.all()
    # retrieve all instructors

    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course_identifier = request.POST.get('course_identifier')
        course_dept = request.POST.get('course_dept')
        course_credits = request.POST.get('course_credits')
        instructor_id = request.POST.get('instructor_id')

        instructor = Instructor.objects.filter(id=instructor_id).first()

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
                instructor=instructor,
                super_id=request.user.supervisor
            )
            messages.success(request, "Course created successfully.")
        except IntegrityError:
            messages.error(request, "An error occurred while creating the course.")

        return redirect('courses-supervisor')


# Edit an existing course
def edit_course(request, course_id):
    context = populate_dict(request)
    course = get_object_or_404(Course, pk=course_id)
    instructors = Instructor.objects.all()

    obj = None
    if user_role == "Supervisor":
        obj = get_object_or_404(Supervisor, user_id=user_id)
    elif user_role == "Instructor":
        obj = get_object_or_404(Instructor, user_id=user_id)
    elif user_role == "TA":
        obj = get_object_or_404(TA, user_id=user_id)

    if request.method == 'POST':
        course.course_name = request.POST.get('course_name')
        course.course_identifier = request.POST.get('course_identifier')
        course.course_dept = request.POST.get('course_dept')
        course.course_credits = request.POST.get('course_credits')
        instructor_id = request.POST.get('instructor_id')
        addTA = request.POST.get('new_course_ta')
        course.save()
        course.course_ta.add(addTA)
        if context['course_name'] != 'None' and cou.first_name != context['fname']:
            did_change = True
            user.fname = context['fname']

        instructor = Instructor.objects.filter(id=instructor_id).first()
        course.instructor = instructor

        course.save()
        return redirect('courses-supervisor')


# Delete a course
def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('courses-supervisor')
    return redirect('courses-supervisor')


def assignTA_course(request):
    context = populate_dict(request)
