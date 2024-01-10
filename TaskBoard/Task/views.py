# views.py

from django.shortcuts import render, redirect ,HttpResponseRedirect,get_object_or_404
from .models import TaskList, Task
from .forms import TaskListForm, TaskForm
from django.http import HttpResponseNotFound
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

def Homepage(request):
    return render(request,'homepage.html')   



class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        # Create a new task list for the logged-in user
        new_task_list = TaskList.objects.create(name=f"{self.request.user.username}'s Task List")
        return reverse_lazy('task_list', kwargs={'task_list_id': new_task_list.id})


class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task_list')
        return super(RegisterPage, self).get(*args, **kwargs)

@login_required(login_url='login')  
def task_list(request):
    task_lists = TaskList.objects.filter(user=request.user)
    tasks = Task.objects.filter(task_list__in=task_lists)

    return render(request, 'task.html', {'task_lists': task_lists, 'tasks': tasks})

class CustomLogoutView(LogoutView):
    template_name = 'logout.html' 



@login_required
def task_detail(request, task_list_id):
    task_list = get_object_or_404(TaskList, pk=task_list_id, user=request.user)
    tasks = Task.objects.filter(task_list=task_list)

    return render(request, 'task.html', {'task_list': task_list, 'tasks': tasks})


# views.py

@login_required
def edit_task(request, task_list_id, task_id):
    task_list = get_object_or_404(TaskList, pk=task_list_id, user=request.user)
    task = get_object_or_404(Task, pk=task_id, task_list=task_list)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_list_id=task_list_id)

    else:
        form = TaskForm(instance=task)

    return render(request, 'edit_task.html', {'form': form, 'task_list': task_list, 'task': task})


# views.py

@login_required
def delete_task(request, task_list_id, task_id):
    task_list = get_object_or_404(TaskList, pk=task_list_id, user=request.user)
    task = get_object_or_404(Task, pk=task_id, task_list=task_list)

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    return render(request, 'delete_task.html', {'task_list': task_list, 'task': task})



# views.py

@login_required
def create_task_list(request):
    if request.method == 'POST':
        form = TaskListForm(request.POST)
        if form.is_valid():
            task_list = form.save(commit=False)
            task_list.user = request.user
            task_list.save()
            return redirect('task_list')
    else:
        form = TaskListForm()

    task_lists = TaskList.objects.filter(user=request.user)
    latest_task_list = task_lists.last()  # Get the latest task list for the current user
    tasks = Task.objects.filter(task_list=latest_task_list)

    return render(request, 'create_task_list.html', {'form': form, 'task_lists': task_lists, 'tasks': tasks, 'task_form': TaskForm(), 'task_list': latest_task_list})


@login_required
def create_task(request, task_list_id):
    task_list = get_object_or_404(TaskList, pk=task_list_id)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.task_list = task_list
            task.save()
            return redirect('task_list')

    else:
        form = TaskForm()

    return render(request, 'create_task.html', {'form': form, 'task_list': task_list})



@login_required
def delete_task_list(request, task_list_id):
    task_list = get_object_or_404(TaskList, pk=task_list_id)

    if request.method == 'POST':
        task_list.delete()
        return redirect('task_list')

    return render(request, 'delete_task_list.html', {'task_list': task_list})