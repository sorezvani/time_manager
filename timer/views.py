from django.shortcuts import render,  get_object_or_404
from .models import Project, State
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Task, TimeEntry, State
from django.utils import timezone
from .forms import TaskForm, ProjectForm

def dashboard(request):
    projects = Project.objects.all().order_by('-id')

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # redirect to clear POST and show updated list
    else:
        form = ProjectForm()

    return render(request, 'dashboard.html', {
        'projects': projects,
        'state_choices': State.CHOICES,  
        'project_form': form,
    })


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    # Create a new TaskForm instance
    task_form = TaskForm()

    if request.method == 'POST':
        # Handle project state change
        if 'project_state' in request.POST:
            project.state = request.POST['project_state']
            project.save()
            return redirect('project_detail', pk=project.pk)

        # Handle task state change
        elif 'task_id' in request.POST and 'task_state' in request.POST:
            task = get_object_or_404(Task, pk=request.POST['task_id'])
            task.state = request.POST['task_state']
            task.save()
            return redirect('project_detail', pk=project.pk)

        # Handle new task creation
        elif 'add_task' in request.POST:
            task_form = TaskForm(request.POST)
            if task_form.is_valid():
                new_task = task_form.save(commit=False)
                new_task.project = project
                new_task.save()
                return redirect('project_detail', pk=project.pk)

    tasks = project.tasks.all().order_by('-id')
    
    return render(request, 'project_detail.html', {
        'project': project,
        'tasks': tasks,
        'state_choices': State.CHOICES,
        'task_form': task_form,
    })

def task_resume(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Check if there's an active TimeEntry for this task (end_time is null)
    active_entry = task.time_entries.filter(end_time__isnull=True).first()

    if request.method == 'POST':
        if 'start' in request.POST:
            # Start a new time entry if no active one exists
            if not active_entry:
                TimeEntry.objects.create(task=task, start_time=timezone.now())
            return redirect('task_resume', task_id=task_id)

        elif 'stop' in request.POST:
            if active_entry:
                active_entry.end_time = timezone.now()
                active_entry.save()
            # Redirect back to project detail page
            return redirect('project_detail', pk=task.project.pk)

    return render(request, 'task_resume.html', {
        'task': task,
        'active_entry': active_entry,
    })

def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('dashboard')