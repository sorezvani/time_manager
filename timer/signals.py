from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import TimeEntry, Task, Project
from datetime import timedelta
from django.db.models import F

# --- We need pre_save to know the OLD value before it's updated ---
@receiver(pre_save, sender=TimeEntry)
def store_old_duration(sender, instance, **kwargs):
    """Store the old duration on the instance before it's saved."""
    if instance.pk:
        try:
            # Get the value from the database *before* the save happens
            instance._old_duration = TimeEntry.objects.get(pk=instance.pk).duration or timedelta(0)
        except TimeEntry.DoesNotExist:
            instance._old_duration = timedelta(0)
    else:
        # This is a new entry
        instance._old_duration = timedelta(0)

# --- post_save handles creation and updates ---
@receiver(post_save, sender=TimeEntry)
def update_durations_on_save(sender, instance, created, **kwargs):
    new_duration = instance.duration or timedelta(0)
    old_duration = instance._old_duration

    # The change in duration is the difference
    duration_diff = new_duration - old_duration

    if duration_diff == timedelta(0):
        return # No change, nothing to do.

    # Apply the difference to the Task and Project
    # Using F() expressions is crucial here to prevent race conditions
    Task.objects.filter(pk=instance.task.pk).update(total_duration=F('total_duration') + duration_diff)
    Project.objects.filter(pk=instance.task.project.pk).update(total_duration=F('total_duration') + duration_diff)

# --- post_delete handles deletions ---
@receiver(post_delete, sender=TimeEntry)
def update_durations_on_delete(sender, instance, **kwargs):
    deleted_duration = instance.duration or timedelta(0)
    
    if deleted_duration == timedelta(0):
        return # Nothing to do

    # Subtract the deleted duration
    Task.objects.filter(pk=instance.task.pk).update(total_duration=F('total_duration') - deleted_duration)
    Project.objects.filter(pk=instance.task.project.pk).update(total_duration=F('total_duration') - deleted_duration)