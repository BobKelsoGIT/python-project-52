from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from task_manager.mixins import AuthRequiredMixin, DeleteProtectionMixin

from .forms import LabelForm
from .models import Label


class ListLabelView(AuthRequiredMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class CreateLabelView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'form.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Label successfully created')
    extra_context = {
        'title': _('Create label'),
        'button_text': _('Create'),
    }


class UpdateLabelView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'form.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Label successfully updated')
    extra_context = {
        'title': _('Update label'),
        'button_text': _('Update'),
    }


class DeleteLabelView(DeleteProtectionMixin, AuthRequiredMixin,
                      SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'delete_form.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Label was successfully deleted')
    protected_url = reverse_lazy('labels_list')
    protected_message = _('This label cannot be deleted because it'
                          'is referenced by other objects.')
    extra_context = {
        'cancel_url': reverse_lazy('labels_list')
    }
