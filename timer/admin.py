from django.contrib import admin
from .models import Project, Task, TimeEntry

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'created_at', 'total_duration')
    list_filter = ('state',)
    search_fields = ('name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'state', 'created_at', 'total_duration')
    list_filter = ('state', 'project')
    search_fields = ('name',)

@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('task', 'start_time', 'end_time', 'duration')
    list_filter = ('task__project',)
    search_fields = ('task__name', 'description')
