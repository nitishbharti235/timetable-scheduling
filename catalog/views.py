import json
import random

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

# importing scheduler class
from .Scheduler import Scheduler

# importing custom forms
from .forms import Input

# importing models
from .models import Course, Classroom, Lecturer, Class, StudentGroup


def get_random_lecturer(lecturers):
    total_lecturer = len(lecturers)
    random_pos = random.randint(0, total_lecturer - 1)
    return lecturers[random_pos]["name"]


@csrf_exempt
def schedule(request):
    if request.method == 'POST':
        input_data = Input(request.POST)
        if input_data.is_valid():
            courses, lecturers, classrooms, student_groups = input_data.clean_jsonfield()

            class_groups = []

            for student_group in student_groups:
                group = student_group["name"]
                group_courses = student_group["courses"]
                for course in group_courses:
                    random_lecturer = get_random_lecturer(lecturers)
                    class_group = [group, course, random_lecturer, 6]
                    class_groups.append(class_group)

            rooms = []
            for classroom in classrooms:
                rooms.append(classroom["name"])

            schedule_t = Scheduler(rooms, class_groups)
            schedule_t.find_fittest()

            print(schedule_t.timeTable)
    return render(request, 'index.html')
