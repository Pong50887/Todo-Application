from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('add/', views.add_todo, name='add_todo'),
    path('signup/', views.signup_view, name='signup'),
    path('update/<int:todo_id>/', views.update_todo_status, name='update_todo_status'),
    path('update_status_ajax/', views.update_status_ajax, name='update_status_ajax'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('edit/<int:todo_id>/', views.edit_todo, name='edit_todo'),

]
