from django import forms
from django.shortcuts import render, redirect, reverse, get_object_or_404, Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators  import login_required
from django.db.models import Count, F

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import *

# class RegistrationView(CreateView):
    
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'register.html'


@login_required
def polling_unit(request):
    if not request.user.is_authenticated:
        raise Http404('Access Denied')

    if request.user.is_admin or request.user.is_superuser:
        raise Http404('Sorry! This is for students only! Login as a student')

    student = get_object_or_404(Student, matric_number=request.user.username)

    # by default fetch presidential candidates
    positions = Position.objects.all()

    current_position = request.GET.get('p', 'president')
    # position = Position.objects.filter(position=current_position)
    position = get_object_or_404(Position, name=current_position)
    choices = Choice.objects.filter(position=position)

    context = {
        'current_position': current_position,
        'positions': positions,
        'choices': choices,
        'student': student,
    }

    return render(request, 'polling_unit.html', context)


def RegistrationView(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            # form.username = request.POST.get('username')

            return redirect('/accounts/login/')
            # return render(request, 'registration/login.html', context={'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', context={'form': form})


@login_required
def CreateVote(request):
    choice_id = request.POST.get('choice_id', None)
    if choice_id is None:
        raise Http404('Select a candidate')
    
    if request.user.is_authenticated:
        student = get_object_or_404(Student, matric_number=request.user.username)

        if Vote.objects.filter(voter=student.id, choice=choice_id).exists():

            return render(request, 'success_vote.html', {'voted': True, 'student': student})

        choice = get_object_or_404(Choice, pk=choice_id)
        try:
            vote = Vote(choice=choice, voter=student)
            vote.save()

            choice.number_of_vote = F('number_of_vote') + 1
            choice.save()
            
        except:
            raise 

        context = {
            'student': student
        }
        return render(request, 'success_vote.html', context)
    raise Http404('Access Denied')


@login_required
def check_result(request):
    if request.user.is_authenticated and request.user.is_admin:

        c = Choice.objects.all()
        return render(request, 'result.html', context={'results': c})
    raise Http404('Access Denied')


import csv
@login_required
def upload_students(request, message=None):
    if not request.user.is_admin:
        raise Http404('Access Denied')
    
    departments = Department.objects.all()

    if request.method == 'GET':
        context = {
            'departments': departments
        }

        return render(request, 'upload_students.html', context)
    
    
    # raise Http404(request.POST.get('department'))
    path = 'students.csv'
 
    students = []
    already_exist = 0
    with open(path, 'r', newline='') as file:
        
        reader = csv.reader(file)
        next(reader, None)

        try:
            department_id = int(request.POST.get('department'))
            department = get_object_or_404(Department, pk=department_id)

            for row in reader:
                if Student.objects.filter(matric_number=row[0]).exists():
                    already_exist +=  1
                    continue
                
                student = Student(
                    matric_number   = row[0],
                    first_name      = row[1],
                    middle_name     = row[2],
                    last_name       = row[3],
                    department      = department
                )
   
                students.append(student)

            s = Student.objects.bulk_create(students)
        except:
            raise
    file.close()
    context = {
            'departments': departments,
            'message': True,
            'success': len(students),
            'error': already_exist
        }
    return render(request, 'upload_students.html', context)




@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password_change')

        else:
            messages.error(request, 'Please correct the error below')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

