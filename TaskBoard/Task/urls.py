from django.urls import path
from .views import task_list, task_detail, create_task_list, create_task, edit_task, delete_task, CustomLoginView, RegisterPage,delete_task_list
from .views import CustomLoginView, RegisterPage, task_list, CustomLogoutView ,LoginView ,LogoutView
from . import views
urlpatterns = [
    path('',views.Homepage,name='Homepage'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  
    path('task-list/', task_list, name='task_list'),
    path('task-list/<int:task_list_id>/', task_detail, name='task_detail'),
    path('register/', RegisterPage.as_view(), name='register'), 
    path('create-task-list/', create_task_list, name='create_task_list'),
    path('create-task/<int:task_list_id>/', create_task, name='create_task'),
    path('edit-task/<int:task_list_id>/<int:task_id>/', edit_task, name='edit_task'),
    path('delete-task/<int:task_list_id>/<int:task_id>/', delete_task, name='delete_task'),
     path('delete-task-list/<int:task_list_id>/', delete_task_list, name='delete_task_list'),
    
]
