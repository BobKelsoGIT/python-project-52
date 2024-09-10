from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import (
    BaseCreateView,
    BaseDeleteView,
    BaseListView,
    BaseUpdateView,
)

from .forms import StatusForm
from .models import Status


class ListStatusView(BaseListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'


class CreateStatusView(BaseCreateView):
    model = Status
    form_class = StatusForm
    success_url_name = 'statuses_list'
    success_message = _('Status successfully created')
    extra_context = {
        'title': _('Create status'),
        'button_text': _('Create'),
    }


class UpdateStatusView(BaseUpdateView):
    model = Status
    form_class = StatusForm
    success_url_name = 'statuses_list'
    success_message = _('Status successfully updated')
    extra_context = {
        'title': _('Update status'),
        'button_text': _('Update'),
    }


class DeleteStatusView(BaseDeleteView):
    model = Status
    success_url_name = 'statuses_list'
    success_message = _('Status successfully deleted')
    protected_url = 'statuses_list'
    protected_message = _('Can not be deleted. In use.')
    extra_context = {
        'cancel_url': reverse_lazy('statuses_list')
    }
