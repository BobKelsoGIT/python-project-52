from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from task_manager.statuses.models import Status

User = get_user_model()


class StatusCRUDTest(TestCase):
    fixtures = [
        'task_manager/tests/fixtures/statuses.json',
        'task_manager/tests/fixtures/users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client.force_login(User.objects.get(pk=1))
        self.status = Status.objects.get(pk=2)

    def test_statuses_list(self):
        response = self.client.get(reverse('statuses_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/index.html')
        self.assertContains(response, self.status.name)

    def test_status_create(self):
        response = self.client.post(reverse('status_create'), {
            'name': 'New Status'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_update(self):
        response = self.client.post(
            reverse('status_update', kwargs={'pk': self.status.pk}),
            {'name': 'Updated Status'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_list'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

    def test_status_delete(self):
        response = self.client.post(
            reverse('status_delete', kwargs={'pk': self.status.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_list'))
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(pk=self.status.pk)
