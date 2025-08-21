from celery import shared_task
from django.utils import timezone
from todo.models import Task
import logging
from django.conf import settings
import asyncio
logger = logging.getLogger(__name__)

@shared_task(name="send_expired_notifications")
def send_expired_notifications():
    tasks = Task.objects.filter(is_completed=False, is_expired=True,is_alerted_expired=False).prefetch_related("telegram_user","category")

    for task in tasks:
        user = task.telegram_user
        if not user:
            continue

        message = (
            f"⚠️ Время на выполнение задачи <b>{task.title}</b> истекло!\n"
            f"🏷 Категория: {task.category.name if task.category else '—'}\n"
            f"🗒 Описание: {task.description or '—'}\n"
            f"⏳ Дедлайн был: {task.due_date.strftime('%d.%m.%Y %H:%M')}"
        )

        try:
            if hasattr(settings.BOT, "send_message"):
                asyncio.run(settings.BOT.send_message(chat_id=user.user_id, text=message, parse_mode="HTML"))
                task.is_alerted_expired = True
                task.save(update_fields=["is_alerted_expired"])
            logger.info(f"Уведомление отправлено пользователю {user.user_id}")
        except Exception as e:
            logger.error(f"Ошибка при отправке уведомления пользователю {user.user_id}: {e}")
