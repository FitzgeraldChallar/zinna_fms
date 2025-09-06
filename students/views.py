from django.shortcuts import render
from .models import Student

def students_by_grade(request, grade):
    students = Student.objects.filter(grade=grade)
    return render(request, 'students/students_by_grade.html', {'students': students, 'grade': grade})
