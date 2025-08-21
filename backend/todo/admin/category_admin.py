from django.contrib import admin
from todo.admin.task_admin import TaskInline
from todo.models import Category

from .mixins import HashidAdminMixin


@admin.register(Category)
class CategoryAdmin(HashidAdminMixin, admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at")
    inlines = [TaskInline]
