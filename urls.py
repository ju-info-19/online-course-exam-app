from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('exam/<int:lesson_id>/', views.take_exam, name='take_exam'),
    path('exam/<int:lesson_id>/submit/', views.submit_exam, name='submit_exam'),  # Chemin pour submit
    path('exam/<int:lesson_id>/result/', views.show_exam_result, name='show_exam_result'),  # Chemin pour show_exam_result
]