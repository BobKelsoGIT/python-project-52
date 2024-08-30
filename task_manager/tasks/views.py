from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from .models import Task
from .task_form import TaskForm


class ListTaskView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'


class CreateTaskView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
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


class UpdateTaskView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'form.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('Task successfully updated')
    extra_context = {
        'title': _('Update task'),
        'button_text': _('Update'),
    }


class DeleteTaskView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'delete_form.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('Task successfully deleted')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionDenied("You are not allowed to delete this task.")
        return obj
