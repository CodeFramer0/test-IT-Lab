from django.contrib import admin
from todo.models import Task

from .mixins import HashidAdminMixin


@admin.register(Task)
class TaskAdmin(HashidAdminMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "telegram_user",
        "category",
        "created_at",
        "due_date",
        "is_completed",
        "is_expired",
        "is_alerted_expired",
    )

    search_fields = (
        "title",
        "description",
        "telegram_user__name",
        "telegram_user__nick_name",
    )

    ordering = ("-created_at",)
    readonly_fields = (
        "id",
        "created_at",
        "is_expired",
        "is_alerted_expired",
    )

    actions = ["mark_done", "mark_undone"]

    @admin.action(description="Отметить выбранные задачи выполненными")
    def mark_done(self, queryset):
        queryset.update(is_completed=True)

    @admin.action(description="Отметить выбранные задачи невыполненными")
    def mark_undone(self, queryset):
        queryset.update(is_completed=False)


class TaskInline(admin.TabularInline):
    model = Task
    fields = ("title", "telegram_user", "due_date", "is_completed")
    readonly_fields = (
        "id",
        "created_at",
    )
    extra = 0
    show_change_link = True
