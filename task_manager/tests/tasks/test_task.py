from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from task_manager.users.models import User
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status


class TaskViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testpass')
        cls.status = Status.objects.create(name='First Status')

    def setUp(self):
        self.client.login(username='testuser', password='testpass')
        self.task = Task.objects.create(name='Test Task', author=self.user, status=self.status)

    def test_tasks_list(self):
        response = self.client.get(reverse('tasks_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')
        self.assertContains(response, self.task.name)

    def test_task_create(self):
        response = self.client.post(reverse('task_create'), {
            'name': 'New Task',
            'description': 'Description',
            'author': self.user,
            'status': self.status.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_list'))
        self.task.refresh_from_db()
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_update(self):
        response = self.client.post(reverse('task_update', args=[self.task.pk]), {
            'name': 'Updated Task',
            'description': 'Updated description',
            'status': self.status.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_list'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')

    def test_task_delete(self):
        response = self.client.post(reverse('task_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_list'))
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(pk=self.task.pk)

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
        response = self.client.post(reverse('task_update', kwargs={'pk': self.task.pk}), {
            'name': 'Updated Task'
        })
        self.assertEqual(response.status_code, 302)
        login_url = reverse('login')
        self.assertTrue(response.url.startswith(login_url))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Test Task')

    def test_task_delete_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse('task_delete', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 302)
        login_url = reverse('login')
        self.assertTrue(response.url.startswith(login_url))
        self.task.refresh_from_db()
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())
