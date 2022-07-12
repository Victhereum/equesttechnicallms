from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic import (View, TemplateView,
                                  ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from base.forms import InstructorProfileForm, StudentProfileForm, MarksForm, MessageForm, NoticeForm, \
    AssignmentForm, SubmitForm, InstructorProfileUpdateForm, StudentProfileUpdateForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponse
from base import models
from base.models import StudentsInClass, StudentMarks, ClassAssignment, SubmitAssignment, Student, Instructors
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q

# For Instructors Sign Up
from equesttechnicallms.users.forms import UserForm, MyUserCreationForm
from equesttechnicallms.users.models import User


def dashboard(request):
    name = request.user
    user = User.objects.get(id=request.user.id)
    dic = {
        'name': name,
        'user': user,
    }
    return render(request, 'classroom/dash.html', context=dic)


def InstructorSignUp(request):
    user_type = 'instructor'
    registered = False

    if request.method == "POST":
        user_form = MyUserCreationForm(data=request.POST)
        teacher_profile_form = InstructorProfileForm(data=request.POST)

        if user_form.is_valid() and teacher_profile_form.is_valid():

            user = user_form.save()
            user.is_teacher = True
            user.save()

            profile = teacher_profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors, teacher_profile_form.errors)
    else:
        user_form = UserForm()
        teacher_profile_form = InstructorProfileForm()

    return render(request, 'classroom/teacher_signup.html',
                  {'user_form': user_form, 'teacher_profile_form': teacher_profile_form, 'registered': registered,
                   'user_type': user_type})


###  For Student Sign Up
def StudentSignUp(request):
    user_type = 'student'
    registered = False

    if request.method == "POST":
        user_form = MyUserCreationForm(data=request.POST)
        student_profile_form = StudentProfileForm(data=request.POST)

        if user_form.is_valid() and student_profile_form.is_valid():

            user = user_form.save()
            user.is_student = True
            user.save()

            profile = student_profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
            return HttpResponseRedirect(reverse('classroom:login'))
        else:
            messages.error(request, 'Sign up failed')
    else:
        user_form = UserForm()
        student_profile_form = StudentProfileForm()

    return render(request, 'classroom/student_signup.html',
                  {'user_form': user_form, 'student_profile_form': student_profile_form, 'registered': registered,
                   'user_type': user_type})


## Sign Up page which will ask whether you are instructor or student.
def SignUp(request):
    return render(request, 'classroom/signup.html', {})


## login view.
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('dashboard'))

            else:
                return HttpResponse("Account not active")

        else:
            messages.error(request, "This user is invalid, try signing up")
            return redirect('classroom:login')
    else:
        return render(request, 'classroom/login.html', {})


## logout view.
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('room-index'))


## User Profile of student.
class StudentDetailView(LoginRequiredMixin, DetailView):
    context_object_name = "student"
    model = models.Student
    template_name = 'classroom/student_detail_page.html'


## User Profile for instructor.
class InstructorDetailView(LoginRequiredMixin, DetailView):
    context_object_name = "instructor"
    model = models.Instructors
    template_name = 'classroom/teacher_detail_page.html'


## Profile update for students.
@login_required
def StudentUpdateView(request, pk):
    profile_updated = False
    student = get_object_or_404(models.Student, pk=pk)
    if request.method == "POST":
        form = StudentProfileUpdateForm(request.POST, instance=student)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'student_profile_pic' in request.FILES:
                profile.student_profile_pic = request.FILES['student_profile_pic']
            profile.save()
            profile_updated = True
    else:
        form = StudentProfileUpdateForm(request.POST or None, instance=student)
    return render(request, 'classroom/student_update_page.html', {'profile_updated': profile_updated, 'form': form})


## Profile update for teachers.
@login_required
def InstructorUpdateView(request, pk):
    profile_updated = False
    instructor = get_object_or_404(models.Instructors, pk=pk)
    if request.method == "POST":
        form = InstructorProfileUpdateForm(request.POST, instance=instructor)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'teacher_profile_pic' in request.FILES:
                profile.teacher_profile_pic = request.FILES['teacher_profile_pic']
            profile.save()
            profile_updated = True
    else:
        form = InstructorProfileUpdateForm(request.POST or None, instance=instructor)
    return render(request, 'classroom/teacher_update_page.html', {'profile_updated': profile_updated, 'form': form})


## List of all students that instructor has added in their class.
def class_students_list(request):
    query = request.GET.get("q", None)
    students = StudentsInClass.objects.filter(instructor=request.user.Instructors)
    students_list = [x.student for x in students]
    qs = Student.objects.all()
    if query is not None:
        qs = qs.filter(
            Q(user__first_name__icontains=query)
        )
    qs_one = []
    for x in qs:
        if x in students_list:
            qs_one.append(x)
        else:
            pass
    context = {
        "class_students_list": qs_one,
    }
    template = "classroom/class_students_list.html"
    return render(request, template, context)


class ClassStudentsListView(LoginRequiredMixin, DetailView):
    model = models.Instructors
    template_name = "classroom/class_students_list.html"
    context_object_name = "instructor"


## For Marks obtained by the student in all subjects.
class StudentAllMarksList(LoginRequiredMixin, DetailView):
    model = models.Student
    template_name = "classroom/student_allmarks_list.html"
    context_object_name = "student"


## To give marks to a student.
@login_required
def add_marks(request, pk):
    marks_given = False
    student = get_object_or_404(models.Student, pk=pk)
    if request.method == "POST":
        form = MarksForm(request.POST)
        if form.is_valid():
            marks = form.save(commit=False)
            marks.student = student
            marks.instructor = request.user.Instructors
            marks.save()
            messages.success(request, 'Marks uploaded successfully!')
            return redirect('base:submit_list')
    else:
        form = MarksForm()
    return render(request, 'classroom/add_marks.html', {'form': form, 'student': student, 'marks_given': marks_given})


## For updating marks.
@login_required
def update_marks(request, pk):
    marks_updated = False
    obj = get_object_or_404(StudentMarks, pk=pk)
    if request.method == "POST":
        form = MarksForm(request.POST, instance=obj)
        if form.is_valid():
            marks = form.save(commit=False)
            marks.save()
            marks_updated = True
    else:
        form = MarksForm(request.POST or None, instance=obj)
    return render(request, 'classroom/update_marks.html', {'form': form, 'marks_updated': marks_updated})


## For writing notice which will be sent to all class students.
@login_required
def add_notice(request):
    notice_sent = False
    instructor = request.user.Instructors
    students = StudentsInClass.objects.filter(instructor=instructor)
    students_list = [x.student for x in students]

    if request.method == "POST":
        notice = NoticeForm(request.POST)
        if notice.is_valid():
            obj = notice.save(commit=False)
            obj.instructor = instructor
            obj.save()
            obj.students.add(*students_list)
            notice_sent = True
    else:
        notice = NoticeForm()
    return render(request, 'classroom/write_notice.html', {'notice': notice, 'notice_sent': notice_sent})


## For student writing message to instructor.
@login_required
def write_message(request, pk):
    message_sent = False
    instructor = get_object_or_404(models.Instructors, pk=pk)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            mssg = form.save(commit=False)
            mssg.instructor = instructor
            mssg.student = request.user.Student
            mssg.save()
            message_sent = True
    else:
        form = MessageForm()
    return render(request, 'classroom/write_message.html',
                  {'form': form, 'instructor': instructor, 'message_sent': message_sent})


## For the list of all the messages instructor have received.
@login_required
def messages_list(request, pk):
    instructor = get_object_or_404(models.Instructors, pk=pk)
    return render(request, 'classroom/messages_list.html', {'instructor': instructor})


## Student can see all notice given by their instructor.
@login_required
def class_notice(request, pk):
    student = get_object_or_404(models.Student, pk=pk)
    return render(request, 'classroom/class_notice_list.html', {'student': student})


## To see the list of all the marks given by the techer to a specific student.
@login_required
def student_marks_list(request, pk):
    error = True
    student = get_object_or_404(models.Student, pk=pk)
    instructor = request.user.Instructors
    given_marks = StudentMarks.objects.filter(instructor=instructor, student=student)
    return render(request, ['classroom/student_marks_list.html'], {'student': student, 'given_marks': given_marks})


## To add student in the class.
class add_student(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('base:students_list')

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(models.Student, pk=self.kwargs.get('pk'))

        try:
            StudentsInClass.objects.create(instructor=self.request.user.Instructors, student=student)
        except:
            messages.warning(self.request, 'warning, Student already in class!')
        else:
            messages.success(self.request, '{} successfully added!'.format(student.user_student_name))

        return super().get(request, *args, **kwargs)


@login_required
def student_added(request):
    return render(request, 'classroom/student_added.html', {})


## List of students which are not added by instructor in their class.
def students_list(request):
    query = request.GET.get("q", None)
    students = StudentsInClass.objects.filter(instructor=request.user.Instructors)
    students_list = [x.student for x in students]
    qs = Student.objects.all()
    if query is not None:
        qs = qs.filter(
            Q(user__first_name__icontains=query)
        )
    qs_one = []
    for x in qs:
        if x in students_list:
            pass
        else:
            qs_one.append(x)

    context = {
        "students_list": qs_one,
    }
    template = "classroom/students_list.html"
    return render(request, "classroom/students_list.html", context)


## List of all the instructor present in the portal.
def teachers_list(request):
    query = request.GET.get("q", None)
    qs = Instructors.objects.all()
    print(qs)

    context = {
        "instructor_list": qs,
    }
    return render(request, "classroom/teachers_list.html", context)


####################################################

## Instructors uploading assignment.
@login_required
def upload_assignment(request):
    assignment_uploaded = False
    teacher = request.user.Instructors
    students = Student.objects.filter(user_student_name__instructor=request.user.Instructors)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=True)
            upload.teacher = teacher
            students = Student.objects.filter(user_student_name__instructor=request.user.Instructors)
            upload.save()
            upload.student.add(*students)
            assignment_uploaded = True
    else:
        form = AssignmentForm()
    return render(request, 'classroom/upload_assignment.html',
                  {'form': form, 'assignment_uploaded': assignment_uploaded})


## Students getting the list of all the assignments uploaded by their instructor.
@login_required
def class_assignment(request):
    student = request.user.Student
    assignment = SubmitAssignment.objects.filter(student=student)
    assignment_list = [x.submitted_assignment for x in assignment]
    return render(request, 'classroom/class_assignment.html', {'student': student, 'assignment_list': assignment_list})


## List of all the assignments uploaded by the instructor himself.
@login_required
def assignment_list(request):
    teacher = request.user.Instructors
    return render(request, 'classroom/assignment_list.html', {'instructor': teacher})


## For updating the assignments later.
@login_required
def update_assignment(request, id=None):
    obj = get_object_or_404(ClassAssignment, id=id)
    form = AssignmentForm(request.POST or None, instance=obj)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=True)
        if 'assignment' in request.FILES:
            obj.assignment = request.FILES['assignment']
        obj.save()
        messages.success(request, "Updated Assignment".format(obj.assignment_name))
        return redirect('classroom:assignment_list')
    template = "classroom/update_assignment.html"
    return render(request, template, context)


## For deleting the assignment.
@login_required
def assignment_delete(request, id=None):
    obj = get_object_or_404(ClassAssignment, id=id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Assignment Removed")
        return redirect('classroom:assignment_list')
    context = {
        "object": obj,
    }
    template = "classroom/assignment_delete.html"
    return render(request, template, context)


## For students submitting their assignment.
@login_required
def submit_assignment(request, id=None):
    student = request.user.Student
    assignment = get_object_or_404(ClassAssignment, id=id)
    teacher = assignment.instructor
    if request.method == 'POST':
        form = SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.teacher = teacher
            upload.student = student
            upload.submitted_assignment = assignment
            upload.save()
            return redirect('classroom:class_assignment')
    else:
        form = SubmitForm()
    return render(request, 'classroom/submit_assignment.html', {'form': form, })


## To see all the submissions done by the students.
@login_required
def submit_list(request):
    teacher = request.user.Instructors
    return render(request, 'classroom/submit_list.html', {'instructor': teacher})


##################################################################################################

## For changing password.
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password changed")
            return redirect('home')
        else:
            return redirect('classroom:change_password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'classroom/change_password.html', args)
