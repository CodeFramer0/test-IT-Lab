from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from todo.filters import TaskFilter
from todo.models import Task
from todo.serializers.task_serializer import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().select_related("telegram_user", "category")
    serializer_class = TaskSerializer
    filterset_class = TaskFilter

    @action(detail=True, methods=["post"])
    def mark_completed(self, request, pk=None):
        task = self.get_object()
        task.is_completed = True
        task.save(update_fields=["is_completed"])
        return Response(self.get_serializer(task).data)

    @action(detail=True, methods=["post"])
    def mark_incomplete(self, request, pk=None):
        task = self.get_object()
        task.is_completed = False
        task.save(update_fields=["is_completed"])
        return Response(self.get_serializer(task).data)
