from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.filter import TaskFilter
from task_manager.tasks.models import Task

User = get_user_model()


class TaskFilterTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()

        cls.user1 = User.objects.create_user(username='user1',
                                             password='password')
        cls.user2 = User.objects.create_user(username='user2',
                                             password='password')

        cls.label1 = Label.objects.create(name='Label1')
        cls.label2 = Label.objects.create(name='Label2')

        cls.status_open = Status.objects.create(name='open')
        cls.status_closed = Status.objects.create(name='closed')

        cls.task1 = Task.objects.create(name='Task 1', author=cls.user1,
                                        executor=cls.user2,
                                        status=cls.status_open)
        cls.task2 = Task.objects.create(name='Task 2', author=cls.user2,
                                        executor=cls.user1,
                                        status=cls.status_closed)
        cls.task2.labels.add(cls.label1)
        cls.task3 = Task.objects.create(name='Task 3', author=cls.user1,
                                        executor=cls.user1,
                                        status=cls.status_open)
        cls.task3.labels.add(cls.label2)

    def test_filter_by_self_tasks(self):
        request = self.factory.get('/tasks/', {'self_tasks': 'on'})
        request.user = self.user1
        filterset = TaskFilter(request.GET, queryset=Task.objects.all(),
                               request=request)
        filtered_qs = filterset.qs
        self.assertEqual(list(filtered_qs), [self.task1, self.task3])

        request = self.factory.get('/tasks/')
        request.user = self.user1
        filterset = TaskFilter(request.GET, queryset=Task.objects.all(),
                               request=request)
        filtered_qs = filterset.qs
        self.assertEqual(list(filtered_qs),
                         [self.task1, self.task2, self.task3])

    def test_filter_by_label(self):
        request = self.factory.get('/tasks/', {'labels': self.label1.id})
        filterset = TaskFilter(request.GET, queryset=Task.objects.all())
        filtered_qs = filterset.qs
        self.assertEqual(list(filtered_qs), [self.task2])

        request = self.factory.get('/tasks/', {'labels': self.label2.id})
        filterset = TaskFilter(request.GET, queryset=Task.objects.all())
        filtered_qs = filterset.qs
        self.assertEqual(list(filtered_qs), [self.task3])

    def test_filter_by_status(self):
        request = self.factory.get('/tasks/', {'status': self.status_open.id})
        filterset = TaskFilter(request.GET, queryset=Task.objects.all())
        filtered_qs = filterset.qs
        self.assertEqual(list(filtered_qs), [self.task1, self.task3])

        request = self.factory.get('/tasks/', {'status': self.status_closed.id})
        filterset = TaskFilter(request.GET, queryset=Task.objects.all())
        filtered_qs = filterset.qs
        self.assertEqual(list(filtered_qs), [self.task2])

    def test_filter_by_executor(self):
        request = self.factory.get('/tasks/', {'executor': self.user1.id})
        filterset = TaskFilter(request.GET, queryset=Task.objects.all())
        filtered_qs = filterset.qs
        self.assertEqual(list(filtered_qs), [self.task2, self.task3])

        request = self.factory.get('/tasks/', {'executor': self.user2.id})
        filterset = TaskFilter(request.GET, queryset=Task.objects.all())
        filtered_qs = filterset.qs
        self.assertEqual(list(filtered_qs), [self.task1])
