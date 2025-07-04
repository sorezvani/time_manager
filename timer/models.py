from django.db import models
from datetime import timedelta
from django.utils import timezone
from django_jalali.db import models as jmodels
from django.core.exceptions import ValidationError

class State:
    END = 'E'
    NEW = 'N'
    RUNNING = 'R'

    CHOICES = [
        (END, 'End'),
        (NEW, 'New'),
        (RUNNING, 'Running'),
    ]

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=1, choices=State.CHOICES, default='N')
    created_at = jmodels.jDateTimeField(default=timezone.now)
    total_duration = models.DurationField(default=timedelta(0), editable=False)

    def __str__(self):
        return self.name
    
class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=1, choices=State.CHOICES, default='N')
    created_at = jmodels.jDateTimeField(default=timezone.now)
    total_duration = models.DurationField(default=timedelta(0), editable=False)
    
    def __str__(self):
        return self.name

class TimeEntry(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='time_entries')
    start_time = jmodels.jDateTimeField(default=timezone.now)
    end_time = jmodels.jDateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    def clean(self):
        if self.end_time and self.start_time:
            if self.end_time < self.start_time:
                raise ValidationError("End time cannot be before start time.")
            self.duration = self.end_time - self.start_time

    def save(self, *args, **kwargs):
        self.clean()  # Auto-run validation & duration
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.task.name} | {self.duration}"