from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/exam/', views.take_exam, name='take_exam'),
    path('course/<int:course_id>/submit/', views.submit_exam, name='submit_exam'),
    path('course/<int:course_id>/result/', views.show_exam_result, name='show_exam_result'),
]
