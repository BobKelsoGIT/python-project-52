from django.urls import path

from .views import (
    CreatStatusView,
    DeleteStatusView,
    ListStatusView,
    UpdateStatusView,
)

urlpatterns = [
    path('', ListStatusView.as_view(), name='statuses_list'),
    path('create/', CreatStatusView.as_view(), name='status_create'),
    path('<int:pk>/update/', UpdateStatusView.as_view(), name='status_update'),
    path('<int:pk>/delete/', DeleteStatusView.as_view(), name='status_delete'),
]
