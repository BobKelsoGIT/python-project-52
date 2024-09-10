from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

User = get_user_model()


class TaskCRUDTest(TestCase):
    fixtures = [
        'task_manager/tests/fixtures/labels.json',
        'task_manager/tests/fixtures/statuses.json',
        'task_manager/tests/fixtures/tasks.json',
        'task_manager/tests/fixtures/users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client.force_login(User.objects.get(pk=1))

    def test_tasks_list(self):
        task = Task.objects.get(pk=4)
        response = self.client.get(reverse('tasks_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')
        self.assertContains(response, task.name)

    def test_task_create(self):
        status = Status.objects.get(pk=2)
        response = self.client.post(reverse('task_create'), {
            'name': 'New Task',
            'description': 'Description',
            'author': self.user.pk,
            'status': status.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_update(self):
        task = Task.objects.get(pk=4)
        status = Status.objects.get(pk=2)
        response = self.client.post(reverse('task_update', args=[task.pk]), {
            'name': 'Updated Task',
            'description': 'Updated description',
            'status': status.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_list'))
        task.refresh_from_db()
        self.assertEqual(task.name, 'Updated Task')

    def test_task_delete(self):
        task = Task.objects.get(pk=4)
        response = self.client.post(reverse('task_delete', args=[task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_list'))
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(pk=task.pk)

    def test_task_create_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse('task_create'), {
            'name': 'New Task'
        })
        self.assertEqual(response.status_code, 302)
        login_url = reverse('login')
        self.assertTrue(response.url.startswith(login_url))
        self.assertFalse(Task.objects.filter(name='New Task').exists())

    def test_task_update_not_logged_in(self):
        self.client.logout()
        task = Task.objects.get(pk=4)
        response = self.client.post(
            reverse('task_update', kwargs={'pk': task.pk}), {
                'name': 'Updated Task'
            })
        self.assertEqual(response.status_code, 302)
        login_url = reverse('login')
        self.assertTrue(response.url.startswith(login_url))
        task.refresh_from_db()
        self.assertEqual(task.name, 'Задача 1')

    def test_task_delete_not_logged_in(self):
        self.client.logout()
        task = Task.objects.get(pk=4)
        response = self.client.post(
            reverse('task_delete', kwargs={'pk': task.pk}))
        self.assertEqual(response.status_code, 302)
        login_url = reverse('login')
        self.assertTrue(response.url.startswith(login_url))
        self.assertTrue(Task.objects.filter(pk=task.pk).exists())
