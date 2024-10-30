# results/urls.py

from django.urls import path
from .views import result_list, student_performance

urlpatterns = [
    path('', result_list, name='result_list'),
    path('performance/', student_performance, name='student_performance'),
]
