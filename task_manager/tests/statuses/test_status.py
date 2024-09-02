from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from task_manager.users.models import User
from task_manager.statuses.models import Status


class StatusViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testpass')

    def setUp(self):
        self.client.login(username='testuser', password='testpass')
        self.status = Status.objects.create(name='Test Status')

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
        self.status.refresh_from_db()
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_update(self):
        response = self.client.post(reverse('status_update', kwargs={'pk': self.status.pk}), {
            'name': 'Updated Status'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_list'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

    def test_status_delete(self):
        response = self.client.post(reverse('status_delete', kwargs={'pk': self.status.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_list'))
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(pk=self.status.pk)

    def test_status_create_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse('status_create'), {
            'name': 'New Status'
        })
        self.assertEqual(response.status_code, 302)
        login_url = reverse('login')
        self.assertTrue(response.url.startswith(login_url))
        self.assertFalse(Status.objects.filter(name='New Status').exists())

    def test_status_update_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse('status_update', kwargs={'pk': self.status.pk}), {
            'name': 'Updated Status'
        })
        self.assertEqual(response.status_code, 302)
        login_url = reverse('login')
        self.assertTrue(response.url.startswith(login_url))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Test Status')

    def test_status_delete_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse('status_delete', kwargs={'pk': self.status.pk}))
        self.assertEqual(response.status_code, 302)
        login_url = reverse('login')
        self.assertTrue(response.url.startswith(login_url))
        self.status.refresh_from_db()
        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())
