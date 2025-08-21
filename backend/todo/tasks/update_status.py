from celery import shared_task
from django.utils import timezone
import pytz
from todo.models import Task
import logging

logger = logging.getLogger(__name__)
TIMEZONE = pytz.timezone("America/Adak")


@shared_task(name="update_task_statuses")
def update_task_statuses():
    now = timezone.now().astimezone(TIMEZONE)
    tasks = Task.objects.filter(is_completed=False, due_date__isnull=False)

    for task in tasks:
        due_date = timezone.localtime(task.due_date, TIMEZONE)
        expired = due_date < now
        
        if task.is_expired != expired:
            task.is_expired = expired
            task.save(update_fields=["is_expired"])