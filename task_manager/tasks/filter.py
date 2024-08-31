import django_filters
from .models import Task
from django import forms
from django.utils.translation import gettext_lazy as _


class TaskFilter(django_filters.FilterSet):
    own_tasks = django_filters.BooleanFilter(
        method='show_own_task',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input mr-3'}),
        label=_('Show own tasks'),
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
        widgets = {
            'status': forms.Select(),
            'executor': forms.Select(),
            'labels': forms.Select()
        }

    def __init__(self, *args, **kwargs):
        super(TaskFilter, self).__init__(*args, **kwargs)
        self.filters['status'].field.widget.attrs.update({'class': 'form-select ml-2 mr-3'})
        self.filters['executor'].field.widget.attrs.update({'class': 'form-select mr-3 ml-2'})
        self.filters['labels'].field.widget.attrs.update({'class': 'form-select mr-3 ml-2'})

    def show_own_task(self, queryset, name, value):
        user = self.request.user if self.request else None
        return queryset.filter(author=user) if value else queryset
