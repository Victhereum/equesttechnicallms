from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, StudentMarks, Instructors, StudentsInClass, CourseCategories, Courses

# Register your models here.

admin.site.register(CourseCategories)
admin.site.register(Courses)
admin.site.register(Student)
admin.site.register(StudentMarks)
admin.site.register(Instructors)
admin.site.register(StudentsInClass)
