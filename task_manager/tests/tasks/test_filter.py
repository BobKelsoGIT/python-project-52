from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.filter import TaskFilter
from task_manager.tasks.models import Task

User = get_user_model()


class TestFilter(TestCase):
    fixtures = [
        'task_manager/tests/fixtures/labels.json',
        'task_manager/tests/fixtures/statuses.json',
        'task_manager/tests/fixtures/tasks.json',
        'task_manager/tests/fixtures/users.json'
    ]

    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.user = User.objects.get(pk=1)
        cls.label = Label.objects.get(pk=4)
        cls.status_new = Status.objects.get(pk=2)
        cls.status_closed = Status.objects.get(pk=4)
        cls.task1 = Task.objects.get(pk=4)
        cls.task2 = Task.objects.get(pk=5)
        cls.task3 = Task.objects.get(pk=7)

    def test_filter_by_self_tasks(self):
        request = self.factory.get('/tasks/', {'self_tasks': 'on'})
        request.user = self.user
        filterset = TaskFilter(request.GET, queryset=Task.objects.all(),
                               request=request)
        filtered_qs = filterset.qs
        self.assertEqual(list(filtered_qs), [self.task1, self.task3])

        request = self.factory.get('/tasks/')
        request.user = self.user
        filterset = TaskFilter(request.GET, queryset=Task.objects.all(),
                               request=request)
        filtered_qs = filterset.qs
        self.assertEqual(list(filtered_qs),
                         [self.task1, self.task2, self.task3])

    def test_filter_by_label(self):
        request = self.factory.get('/tasks/', {'labels': self.label.pk})
        filterset = TaskFilter(request.GET, queryset=Task.objects.all())
        filtered_qs = filterset.qs
        self.assertEqual(list(filtered_qs), [self.task3])

    def test_filter_by_status(self):
        request = self.factory.get('/tasks/', {'status': self.status_new.pk})
        filterset = TaskFilter(request.GET, queryset=Task.objects.all())
        filtered_qs = filterset.qs
        self.assertEqual(list(filtered_qs), [self.task1])

        request = self.factory.get('/tasks/', {'status': self.status_closed.pk})
        filterset = TaskFilter(request.GET, queryset=Task.objects.all())
        filtered_qs = filterset.qs
        self.assertEqual(list(filtered_qs), [self.task3])
