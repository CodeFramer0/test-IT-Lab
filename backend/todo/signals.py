from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Category


@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    if not Category.objects.exists():
        Category.objects.create(name="Важно")
        Category.objects.create(name="Личное")

    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin",
        )
