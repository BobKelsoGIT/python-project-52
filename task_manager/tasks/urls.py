from django.urls import path

from .views import (
    CreateTaskView,
    DeleteTaskView,
    DetailTaskView,
    ListTaskView,
    UpdateTaskView,
)

urlpatterns = [
    path('', ListTaskView.as_view(), name='tasks_list'),
    path('create/', CreateTaskView.as_view(), name='task_create'),
    path('<int:pk>/update/', UpdateTaskView.as_view(), name='task_update'),
    path('<int:pk>/delete/', DeleteTaskView.as_view(), name='task_delete'),
    path('<int:pk>/', DetailTaskView.as_view(), name='task_detail'),
]
