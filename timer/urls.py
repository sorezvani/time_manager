from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('task/<int:task_id>/resume/', views.task_resume, name='task_resume'),
    path('project/add/', views.add_project, name='add_project'),
]
