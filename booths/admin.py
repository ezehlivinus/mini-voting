from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import *


# class UserCreationForm(forms.ModelForm):
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

#     class Meta:
#         model = CustomUser
#         fields = ('email', 'username')



# admin.site.register(CustomUser, UserAdmin)


# admin.site.unregister(Group)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    readonly_fields = ['password']
    # defines which should appear as a column name(s) and it data shown as a lists of records(rows)
    list_display = ['username', 'email', 'is_admin', 'is_superuser', 'is_staff']
    # defines filter column
    list_filter = ['username', 'is_admin']
    search_fields = ['username']



@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # readonly_fields = ['total']
    search_fields = ['last_name', 'first_name', 'middle_name', 'matric_number']
    # defines which should appear as a column name(s) and it data shown as a lists of records(rows)
    list_display = ['last_name', 'first_name', 'middle_name', 'matric_number']
    # defines filter column
    list_filter = ['last_name', 'first_name']
    # defines how the list would be ordered
    ordering = ('last_name', 'first_name')


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    # defines which should appear as a column name(s) and it data shown as a lists of records(rows)
    list_display = ['name']
    # defines filter column
    list_filter = ['name']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ['name']
    # defines which should appear as a column name(s) and it data shown as a lists of records(rows)
    list_display = ['name', 'faculty']
    # defines filter column
    list_filter = ['name']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    search_fields = ['name']
    # defines which should appear as a column name(s) and it data shown as a lists of records(rows)
    list_display = ['name']
    # defines filter column
    list_filter = ['name']


# @admin.register(Poll)
# class PollAdmin(admin.ModelAdmin):
#     search_fields = ['title']
#     # defines which should appear as a column name(s) and it data shown as a lists of records(rows)
#     list_display = ['title', 'description', 'author', 'session']
#     # defines filter column
#     list_filter = ['title', 'author', 'session']



@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ['name']
    # defines which should appear as a column name(s) and it data shown as a lists of records(rows)
    list_display = ['name', 'description']


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    readonly_fields = ['number_of_vote']

    search_fields = ['candidate', 'position']
    # defines which should appear as a column name(s) and it data shown as a lists of records(rows)
    list_display = ['candidate', 'position', 'description', 'number_of_vote']
    # defines filter column
    list_filter = ['candidate', 'position', 'number_of_vote']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    search_fields = [ 'candidate', 'position']
    # defines which should appear as a column name(s) and it data shown as a lists of records(rows)
    list_display = ['choice', 'voter']
    # defines filter column
    list_filter = ['voter', 'choice']

