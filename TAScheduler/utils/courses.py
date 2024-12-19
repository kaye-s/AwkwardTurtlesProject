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
        'section_type': escape(request.POST.get('section_type')),
        'section_num': escape(request.POST.get('section_num')),
        'section_course': escape(request.POST.get('section_course')),
        'days_of_week': escape(request.POST.get('days_of_week')),
        'section_startTime': escape(request.POST.get('section_startTime')),
        'section_endTime': escape(request.POST.get('section_endTime')),
        'section_ta': escape(request.POST.get('section_ta')),
        'lecture_instructor': escape(request.POST.get('lecture_instructor')),
    }


def create_course(request):
    context = populate_dict(request)

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
        instructorPass = Instructor.objects.get(user=context['instructor'])
        Course.objects.create(
            course_name=context['course_name'],
            course_identifier=context['course_identifier'],
            course_dept=context['course_dept'],
            course_credits=context['course_credits'],
            instructor=instructorPass,
            super_id=Supervisor.objects.get(user=request.user),
        )
        messages.success(request, "Course created successfully.")
    return redirect('courses-supervisor')


# Edit an existing course
def edit_course(request, course_id):
    course = Course.objects.get(course_id=course_id)
    did_change = False
    context = populate_dict(request)
    if context['course_identifier'] != 'None' and course.course_identifier != context['course_identifier']:
        if Course.objects.filter(course_identifier=context['course_identifier']).exists():
            messages.error(request, f"A course with the identifier '{context['course_identifier']}' already exists.")
            return redirect('courses-supervisor')
        did_change = True
        course.course_identifier = context['course_identifier']
    if context['course_name'] != 'None' and course.course_name != context['course_name']:
        did_change = True
        course.course_name = context['course_name']
    if context['course_dept'] != 'None' and course.course_dept != context['course_dept']:
        did_change = True
        course.course_dept = context['course_dept']
    if context['course_credits'] != 'None' and course.course_credits != context['course_credits']:
        did_change = True
        course.course_credits = context['course_credits']
    if context['instructor'] != 'None' and course.instructor != context['instructor']:
        did_change = True
        instructorPass = Instructor.objects.get(context['instructor'])
        course.instructor = instructorPass
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

def assignTA_course(request, course_id):
    tas = TA.objects.all()
    context = populate_dict(request)
    course = Course.objects.filter(course_id=course_id).exists()
    if course:
        course = Course.objects.get(course_id=course_id)
    if not Course.objects.filter(course_id=course_id, course_ta=context['course_ta']).exists():
        course.course_ta.add(context['course_ta'])
        course.save()
        messages.success(request, "TA successfully added to course.")
    else:
        messages.error(request, "TA already assigned to this course")
    return redirect('courses-supervisor')

def removeTA_course(request, course_id):
    context = populate_dict(request)
    course = Course.objects.filter(course_id=course_id).exists()
    if course:
        course = Course.objects.get(course_id=course_id)
    if Course.objects.filter(course_id=course_id, course_ta=context['course_ta']).exists():
        course.course_ta.remove(context['course_ta'])
        course.save()
        messages.success(request, "TA  successfully removed from course.")
    else:
        messages.error(request, "TA is not assigned to this course - cannot remove")
    return redirect('courses-supervisor')

def create_section(request):
    context = populate_dict(request)

    # Check if a course with the same identifier already exists
    if Section.objects.filter(section_num=context['section_num']).exists():
        messages.error(request, f"A section with the identifier '{context['section_num']}' already exists.")
        return redirect('courses-supervisor')

    if context['lecture_instructor'] == 'None':
        context['lecture_instructor'] = None
    else:
        context['lecture_instructor'] = Instructor.objects.get(id=context['lecture_instructor'])
    if context['section_ta'] == 'None':
        context['section_ta'] = None
    else:
        context['section_ta'] = TA.objects.get(id=context['section_ta'])


    course = Course.objects.get(course_id=context['course_id'])
    if course.instructor != context['lecture_instructor'] and context['lecture_instructor'] != None:
        messages.error(request, f"This instructor isn't a part of that course. Please be sure to only select instructors that are assigned to the course.")
        return redirect('courses-supervisor')
    if context['section_ta'] not in course.course_ta.all() and context['section_ta'] != None:
        messages.error(request, f"This TA isn't a part of that course. Please be sure to only select TAs that are assigned to the course.")
        return redirect('courses-supervisor')

    # Create the course if no duplicate is found
    Section.objects.create(
        section_type=context['section_type'],
        section_num=context['section_num'],
        section_course=Course.objects.get(course_id=context['course_id']),
        days_of_week=context['days_of_week'],
        section_startTime=context['section_startTime'],
        section_endTime=context['section_endTime'],
        section_ta=context['section_ta'],
        lecture_instructor=context['lecture_instructor'],
    )
    messages.success(request, "Section created successfully.")

    return redirect('courses-supervisor')

def delete_section(request, section_id):
    section = Section.objects.filter(section_id=section_id).exists()
    if section:
        Section.objects.get(section_id=section_id).delete()
        return redirect('courses-supervisor')
    else:
        messages.error(request, "Section does not exist")
        return redirect('courses-supervisor')

def edit_section(request, section_id):
    pass


