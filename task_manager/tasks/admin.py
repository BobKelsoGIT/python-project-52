from django.contrib import admin

from .models import Task, TaskLabelRelation


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'author', 'date_created', 'status', 'executor',
        'display_labels',
    )

    def display_labels(self, obj):
        labels = (TaskLabelRelation.objects.filter
                  (task=obj).select_related('label'))
        return ', '.join(
            [label_relation.label.name for label_relation in labels]
        )

    display_labels.short_description = 'Labels'


@admin.register(TaskLabelRelation)
class TaskRelationsAdmin(admin.ModelAdmin):
    list_display = ('task', 'label')
