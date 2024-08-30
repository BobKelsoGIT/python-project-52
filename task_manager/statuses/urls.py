from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListStatusView.as_view(), name='statuses_list'),
    path('create/', views.CreatStatusView.as_view(), name='status_create'),
    path('<int:pk>/update/', views.UpdateStatusView.as_view(), name='status_update'),
    path('<int:pk>/delete/', views.DeleteStatusView.as_view(), name='status_delete'),
]