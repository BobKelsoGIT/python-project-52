from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import (
    BaseCreateView,
    BaseDeleteView,
    BaseListView,
    BaseUpdateView,
)

from .forms import LabelForm
from .models import Label


class ListLabelView(BaseListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class CreateLabelView(BaseCreateView):
    model = Label
    form_class = LabelForm
    success_url_name = 'labels_list'
    success_message = _('Label successfully created')
    extra_context = {
        'title': _('Create label'),
        'button_text': _('Create'),
    }


class UpdateLabelView(BaseUpdateView):
    model = Label
    form_class = LabelForm
    success_url_name = 'labels_list'
    success_message = _('Label successfully updated')
    extra_context = {
        'title': _('Update label'),
        'button_text': _('Update'),
    }


class DeleteLabelView(BaseDeleteView):
    model = Label
    success_url_name = 'labels_list'
    success_message = _('Label was successfully deleted')
    protected_url = 'labels_list'
    protected_message = _('This label cannot be deleted because it'
                          'is referenced by other objects.')
    extra_context = {
        'cancel_url': reverse_lazy('labels_list')
    }
