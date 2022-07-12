from django import forms
from django.contrib.auth.forms import UserCreationForm
from base.models import User, Instructors, Student, StudentMarks, MessageToInstructor, ClassNotice, ClassAssignment, \
    SubmitAssignment
from django.db import transaction


# Instructors Registration Form
class InstructorProfileForm(forms.ModelForm):
    class Meta:
        model = Instructors
        fields = '__all__'
        widgets = {
            'course': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Instructors Profile Update Form
class InstructorProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Instructors
        fields = '__all__'


# Student Registration Form
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['birthday', 'gender']
        widgets = {

        }


# Student profile update form
class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'


# Form for uploading marks and also for updating it.
class MarksForm(forms.ModelForm):
    class Meta:
        model = StudentMarks
        fields = ['course', 'marks_obtained', 'maximum_marks']


# Writing message to instructor
class MessageForm(forms.ModelForm):
    class Meta:
        model = MessageToInstructor
        fields = ['message']


# Writing notice in the class
class NoticeForm(forms.ModelForm):
    class Meta:
        model = ClassNotice
        fields = ['message']


# Form for uploading or updating assignment (teachers only)
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = ClassAssignment
        fields = ['assignment_name', 'assignment']


# Form for submitting assignment (Students only)
class SubmitForm(forms.ModelForm):
    class Meta:
        model = SubmitAssignment
        fields = ['submit']
