from django.urls import path
from . import views

urlpatterns = [
    path('grade/<str:grade>/', views.students_by_grade, name='students_by_grade'),
]
