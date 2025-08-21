from django.db import connection
from django.db.utils import OperationalError
from django.http import JsonResponse
from django.urls import path
from rest_framework.routers import DefaultRouter

from .viewsets import *


def healthcheck(request):
    try:
        connection.ensure_connection()
        db_status = "ok"
    except OperationalError:
        db_status = "error"

    return JsonResponse({"status": "ok", "database": db_status, "version": "1.0.0"})


router = DefaultRouter()

viewsets = [
    (r"categories", CategoryViewSet),
    (r"tasks", TaskViewSet),
    (r"telegram-users", TelegramUserViewSet),
]

for prefix, viewset in viewsets:
    router.register(prefix, viewset, basename=prefix)

urlpatterns = router.urls
urlpatterns += [
    path("health/", healthcheck),
]
