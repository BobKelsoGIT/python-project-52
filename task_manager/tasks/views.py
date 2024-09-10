from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django_filters.views import FilterView
from task_manager.mixins import (
    AuthorDeletionMixin,
    AuthRequiredMixin,
    BaseCreateView,
    BaseDeleteView,
    BaseUpdateView,
)

from .filter import TaskFilter
from .forms import TaskForm
from .models import Task


class ListTaskView(AuthRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class DetailTaskView(AuthRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'
    extra_context = {
        'title': _('Task details'),
        'Task details': _('Task details')
    }


class CreateTaskView(BaseCreateView):
    model = Task
    form_class = TaskForm
    success_url_name = 'tasks_list'
    success_message = _('Task successfully created')
    extra_context = {
        'title': _('Tasks'),
        'button_text': _('Create'),
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTaskView(AuthRequiredMixin, BaseUpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'components/form.html'
    success_url_name = 'tasks_list'
    success_message = _('Task successfully updated')
    extra_context = {
        'title': _('Update task'),
        'button_text': _('Update'),
    }


class DeleteTaskView(AuthRequiredMixin, AuthorDeletionMixin, BaseDeleteView):
    model = Task
    success_url_name = 'tasks_list'
    success_message = _('Task successfully deleted')
    auth_message = _('Log in please!')
    author_message = _("Task can be deleted only by it's author!")
    author_url = reverse_lazy('tasks_list')
    extra_context = {
        'cancel_url': reverse_lazy('tasks_list')
    }
