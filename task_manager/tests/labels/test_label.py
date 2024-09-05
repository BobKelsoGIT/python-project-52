from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task, TaskLabelRelation

User = get_user_model()


class LabelViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser',
                                            password='testpass')

    def setUp(self):
        self.client.login(username='testuser', password='testpass')
        self.label = Label.objects.create(name='Test Label')

    def test_labels_list(self):
        response = self.client.get(reverse('labels_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/index.html')
        self.assertContains(response, self.label.name)

    def test_label_create(self):
        response = self.client.post(reverse('label_create'), {
            'name': 'New Label'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_list'))
        self.label.refresh_from_db()
        self.assertTrue(Label.objects.filter(name='New Label').exists())

    def test_label_update(self):
        response = self.client.post(reverse('label_update',
                                            args=[self.label.pk]), {
                                        'name': 'Updated Label'
                                    })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_list'))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')

    def test_label_delete(self):
        response = self.client.post(reverse('label_delete',
                                            args=[self.label.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_list'))
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(pk=self.label.pk)

    def test_label_delete_protected_error(self):
        protected_label = Label.objects.create(name='Referenced Label')
        Status.objects.create(name='First Status')
        task = Task.objects.create(
            name='Test Task',
            description='Task description',
            author=self.user,
            status=Status.objects.first()
        )
        TaskLabelRelation.objects.create(task=task, label=protected_label)

        response = self.client.post(reverse('label_delete',
                                            args=[protected_label.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels_list'))
        self.assertTrue(Label.objects.filter(pk=protected_label.pk).exists())

    def test_label_create_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse('label_create'), {
            'name': 'New Label'
        })
        self.assertEqual(response.status_code, 302)
        login_url = reverse('login')
        self.assertTrue(response.url.startswith(login_url))
        self.assertFalse(Label.objects.filter(name='New Label').exists())

    def test_label_update_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse('label_update',
                                            kwargs={'pk': self.label.pk}), {
                                        'name': 'Updated Label'
                                    })
        self.assertEqual(response.status_code, 302)
        login_url = reverse('login')
        self.assertTrue(response.url.startswith(login_url))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Test Label')

    def test_label_delete_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse('label_delete',
                                            kwargs={'pk': self.label.pk}))
        self.assertEqual(response.status_code, 302)
        login_url = reverse('login')
        self.assertTrue(response.url.startswith(login_url))
        self.label.refresh_from_db()
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())
