from django.db import models
from hashid_field import HashidAutoField

from .category import Category
from .telegram_user import TelegramUser


class Task(models.Model):
    id = HashidAutoField(
        primary_key=True,
        salt="task_salt",
        min_length=12,
        verbose_name="ID",
    )
    telegram_user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tasks",
        verbose_name="Telegram пользователь",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Категория",
    )
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    due_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Срок выполнения"
    )
    is_completed = models.BooleanField(default=False, verbose_name="Выполнена")
    is_expired = models.BooleanField(default=False, verbose_name="Просрочена")
    is_alerted_expired = models.BooleanField(
        default=False, verbose_name="Уведомление о просрочке отправлено"
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["created_at"]

    def __str__(self):
        return self.title
