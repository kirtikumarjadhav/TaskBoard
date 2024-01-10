# forms.py

from django import forms
from .models import TaskList, Task

class TaskListForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ['name']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'completed']
