from django.views.generic import (ListView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import AuthRequiredMixin, DeleteProtectionMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .models import Status
from .status_form import StatusForm


class ListStatusView(AuthRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'


class CreatStatusView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'form.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Status successfully created')
    extra_context = {
        'title': _('Create status'),
        'button_text': _('Create'),
    }


class UpdateStatusView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'form.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Status successfully updated')
    extra_context = {
        'title': _('Update status'),
        'button_text': _('Update'),
    }


class DeleteStatusView(AuthRequiredMixin, DeleteProtectionMixin,
                       SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'delete_form.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Status successfully deleted')
    protected_message = _('Can not be deleted. In use.')
    protected_url = reverse_lazy('statuses_list')
    extra_context = {
        'cancel_url': reverse_lazy('statuses_list')
    }
