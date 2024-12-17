from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils.html import escape
from django.db import IntegrityError
from django.utils.translation.template import blankout

from TAScheduler.models import *


def populate_dict(request):
    return {
        'course_id': escape(request.POST.get('course_id')),
        'super_id': escape(request.POST.get('super_id')),
        'course_name': escape(request.POST.get('course_name')),
        'course_identifier': escape(request.POST.get('course_identifier')),
        'course_dept': escape(request.POST.get('course_dept')),
        'course_credits': escape(request.POST.get("course_credits")),
        'course_ta': escape(request.POST.get("course_ta")),
        'instructor': escape(request.POST.get("instructor")),
        'action': escape(request.POST.get('action')),
    }


def create_course(request):
    instructors = Instructor.objects.all()
    context = populate_dict(request)
    # retrieve all instructors

    # instructor = Instructor.objects.filter(id=instructor_id).first()

    # Check if a course with the same identifier already exists
    if Course.objects.filter(course_identifier=context['course_identifier']).exists():
        messages.error(request, f"A course with the identifier '{context['course_identifier']}' already exists.")
        return redirect('courses-supervisor')

    # Create the course if no duplicate is found
    if context['instructor'] == 'None':
        Course.objects.create(
            course_name=context['course_name'],
            course_identifier=context['course_identifier'],
            course_dept=context['course_dept'],
            course_credits=context['course_credits'],
            super_id=Supervisor.objects.get(user=request.user),
        )
        messages.success(request, "Course created successfully.")
    else:
        Course.objects.create(
            course_name=context['course_name'],
            course_identifier=context['course_identifier'],
            course_dept=context['course_dept'],
            course_credits=context['course_credits'],
            instructor=context['instructor'],
            super_id=Supervisor.objects.get(user=request.user),
        )

    return redirect('courses-supervisor')


# Edit an existing course
def edit_course(request, course_id):
    course = Course.objects.get(course_id=course_id)

    context = populate_dict(request)

    if context['course_name'] != 'None' and course.course_name != context['course_name']:
        did_change = True
        course.course_name = context['course_name']
    if context['course_dept'] != 'None' and course.course_dept != context['course_dept']:
        did_change = True
        course.course_dept = context['course_dept']
    if context['course_identifier'] != 'None' and course.course_identifier != context['course_identifier']:
        did_change = True
        course.course_identifier = context['course_identifier']
    if context['course_credits'] != 'None' and course.course_credits != context['course_credits']:
        did_change = True
        course.course_credits = context['course_credits']
    if context['instructor'] != 'None' and course.instructor != context['instructor']:
        did_change = True
        course.instructor = context['instructor']
    #if context['new_course_ta'] != 'None':
    #    alreadyExists = 'None'
    #    if not Course.objects.filter(course_ta=context['new_course_ta']).exists():
    #        Course.objects.add(course_ta=context['new_course_ta'])

    if did_change:
        course.save()

    course.save()
    return redirect('courses-supervisor')


# Delete a course
def delete_course(request, course_id):
    course = Course.objects.filter(course_id=course_id).exists()
    if course:
        Course.objects.get(course_id=course_id).delete()
        return redirect('courses-supervisor')
    else:
        messages.error(request, "Course does not exist")
        return redirect('courses-supervisor')


def assignTA_course(request):
    context = populate_dict(request)
