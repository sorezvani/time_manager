from django import forms
from .models import Task, Project

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'state']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'state']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }