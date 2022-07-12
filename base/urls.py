from django.urls import path
from base import views

app_name = 'base'

urlpatterns = [
    path('signup/', views.SignUp, name="signup"),
    path('signup/student_signup/', views.StudentSignUp, name="StudentSignUp"),
    path('signup/teacher_signup/', views.InstructorSignUp, name="InstructorSignUp"),
    # path('login/', views.user_login, name="login"),
    # path('logout/', views.user_logout, name="logout"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('student/<int:pk>/', views.StudentDetailView.as_view(), name="student_detail"),
    path('instructor/<int:pk>/', views.InstructorDetailView.as_view(), name="teacher_detail"),
    path('update/student/<int:pk>/', views.StudentUpdateView, name="student_update"),
    path('update/instructor/<int:pk>/', views.InstructorUpdateView, name="teacher_update"),
    path('student/<int:pk>/enter_marks', views.add_marks, name="enter_marks"),
    path('student/<int:pk>/marks_list', views.student_marks_list, name="student_marks_list"),
    path('marks/<int:pk>/update', views.update_marks, name="update_marks"),
    path('student/<int:pk>/add', views.add_student.as_view(), name="add_student"),
    path('student_added/', views.student_added, name="student_added"),
    path('students_list/', views.students_list, name="students_list"),
    path('teachers_list/', views.teachers_list, name="teachers_list"),
    path('instructor/class_students_list', views.class_students_list, name="class_student_list"),
    path('student/<int:pk>/all_marks', views.StudentAllMarksList.as_view(), name="all_marks_list"),
    path('student/<int:pk>/message', views.write_message, name="write_message"),
    path('instructor/<int:pk>/messages_list', views.messages_list, name="messages_list"),
    path('instructor/write_notice', views.add_notice, name="write_notice"),
    path('student/<int:pk>/class_notice', views.class_notice, name="class_notice"),
    path('upload_assignment/', views.upload_assignment, name="upload_assignment"),
    path('class_assignment/', views.class_assignment, name="class_assignment"),
    path('assignment_list/', views.assignment_list, name="assignment_list"),
    path('update_assignment/<int:id>/', views.update_assignment, name="update_assignment"),
    path('assignment_delete/<int:id>/', views.assignment_delete, name="assignment_delete"),
    path('submit_assignment/<int:id>/', views.submit_assignment, name="submit_assignment"),
    path('submit_list/', views.submit_list, name="submit_list"),
    path('change_password/', views.change_password, name="change_password"),

]
