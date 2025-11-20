"""
URL configuration for the core app - Task Management System.
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Page routes
    path('', views.home, name='home'),
    path('tasks/', views.task_list_view, name='task_list'),
    path('tasks/create/', views.task_create_view, name='task_create'),
    path('tasks/<int:task_id>/', views.task_detail_view, name='task_detail'),
    path('tasks/<int:task_id>/edit/', views.task_edit_view, name='task_edit'),
    
    # Authentication routes
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # API routes - Task Management
    path('api/status/', views.status_endpoint, name='status'),
    path('api/search/', views.search_tasks_endpoint, name='search_tasks'),
    path('api/tasks/', views.task_list_endpoint, name='task_list_api'),
    path('api/tasks/<int:task_id>/', views.task_detail_endpoint, name='task_detail_api'),
    path('api/tasks/create/', views.task_create_endpoint, name='task_create_api'),
    path('api/tasks/<int:task_id>/update/', views.task_update_endpoint, name='task_update_api'),
    path('api/tasks/<int:task_id>/delete/', views.task_delete_endpoint, name='task_delete_api'),
]
