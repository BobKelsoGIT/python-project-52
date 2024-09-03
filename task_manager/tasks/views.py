from django.views.generic import (CreateView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import AuthRequiredMixin, AuthorDeletionMixin
from django.utils.translation import gettext_lazy as _
from django_filters.views import FilterView
from django.urls import reverse_lazy
from .models import Task
from .task_form import TaskForm
from .filter import TaskFilter


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


class CreateTaskView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'form.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('Task successfully created')
    extra_context = {
        'title': _('Tasks'),
        'button_text': _('Create'),
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTaskView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'form.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('Task successfully updated')
    extra_context = {
        'title': _('Update task'),
        'button_text': _('Update'),
    }


class DeleteTaskView(AuthRequiredMixin, AuthorDeletionMixin,
                     SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'delete_form.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('Task successfully deleted')
    auth_message = _('Log in please!')
    author_message = _("Task can be deleted only by it's author!")
    author_url = reverse_lazy('tasks_list')
    extra_context = {
        'cancel_url': reverse_lazy('tasks_list')
    }
