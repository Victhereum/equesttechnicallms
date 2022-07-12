from django.db import models
from equesttechnicallms.users.models import User
from django.urls import reverse
from django.conf import settings


GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

COURSE_LEVEL = (
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced')
)


class CourseCategories(models.Model):
    name = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.name


class Courses(models.Model):
    category = models.ForeignKey(CourseCategories, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    level = models.CharField(max_length=20, choices=COURSE_LEVEL, default=COURSE_LEVEL[0][0])
    cover_image = models.ImageField(upload_to='courses/cover_images/',
                                    default='equesttechnicallms/static/img/brand/favicon.png')
    logo = models.ImageField(upload_to='courses/logo/', default='equesttechnicallms/static/img/brand/favicon.png')



    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='Student')
    birthday = models.DateField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10)
    joined = models.DateField(auto_created=True)

    def get_absolute_url(self):
        return reverse('base:student_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        ordering = ['-joined']


class Instructors(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='Instructors')
    course_category = models.ForeignKey(CourseCategories, on_delete=models.CASCADE, related_name='course')
    class_students = models.ManyToManyField(Student, through="StudentsInClass")

    def get_absolute_url(self):
        return reverse('base:teacher_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.user.get_full_name()


class StudentMarks(models.Model):
    instructor = models.ForeignKey(Instructors, related_name='given_marks', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name="marks", on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField()
    maximum_marks = models.IntegerField()

    def __str__(self):
        return self.course


class StudentsInClass(models.Model):
    instructor = models.ForeignKey(Instructors, related_name="class_teacher", on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name="user_student_name", on_delete=models.CASCADE)

    def __str__(self):
        return self.student.user.get_full_name()

    class Meta:
        unique_together = ('instructor', 'student')


class MessageToInstructor(models.Model):
    student = models.ForeignKey(Student, related_name='student', on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructors, related_name='messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)

    def __str__(self):
        return self.message

    # def save(self, *args, **kwargs):
    #     self.message_html = misaka.html(self.message)
    #     super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['student', 'message']


class ClassNotice(models.Model):
    instructor = models.ForeignKey(Instructors, related_name='instructor', on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='class_notice')
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-created_at']
        unique_together = ['instructor', 'message']


class ClassAssignment(models.Model):
    student = models.ManyToManyField(Student, related_name='student_assignment')
    instructor = models.ForeignKey(Instructors, related_name='teacher_assignment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    assignment_name = models.CharField(max_length=250)
    assignment = models.FileField(upload_to='assignments')

    def __str__(self):
        return self.assignment_name

    class Meta:
        ordering = ['-created_at']


class SubmitAssignment(models.Model):
    student = models.ForeignKey(Student, related_name='student_submit', on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructors, related_name='teacher_submit', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    submitted_assignment = models.ForeignKey(ClassAssignment, related_name='submission_for_assignment',
                                             on_delete=models.CASCADE)
    submit = models.FileField(upload_to='Submission')

    def __str__(self):
        return "Submitted" + str(self.submitted_assignment.assignment_name)

    class Meta:
        ordering = ['-created_at']
