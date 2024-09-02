from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Label
from .label_form import LabelForm
from django.db.models import ProtectedError
from django.contrib import messages


class ListLabelView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class CreateLabelView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'form.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Label successfully created')
    extra_context = {
        'title': _('Create label'),
        'button_text': _('Create'),
    }


class UpdateLabelView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'form.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Label successfully updated')
    extra_context = {
        'title': _('Update label'),
        'button_text': _('Update'),
    }


class DeleteLabelView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'delete_form.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Label successfully deleted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('labels_list')
        return context

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError as e:
            messages.error(request, _('This label cannot be deleted because it is referenced by other objects.'))
            return HttpResponseRedirect(reverse_lazy('labels_list'))
