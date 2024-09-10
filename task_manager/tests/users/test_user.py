from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserCRUDTest(TestCase):
    fixtures = ['task_manager/tests/fixtures/users.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client.force_login(User.objects.get(pk=1))

    def test_user_list_view(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')
        self.assertContains(response, 'VlaPut')

    def test_user_create(self):
        response = self.client.get(reverse('user_create'))
        self.assertTemplateUsed(response, 'components/form.html')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('user_create'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'first_name': 'New',
            'last_name': 'User'
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_update(self):

        response = self.client.get(
            reverse('user_update', kwargs={'pk': self.user.pk}))
        self.assertTemplateUsed(response, 'components/form.html')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('user_update', kwargs={'pk': self.user.pk}), {
                'first_name': 'Updated',
                'last_name': 'Name',
                'username': self.user.username,
                'password1': 'test1pass',
                'password2': 'test1pass',
            })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')

    def test_user_update_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse('user_update',
                                            kwargs={'pk': self.user.pk}), {
                                        'first_name': 'Unauthorized',
                                        'last_name': 'Update'
                                    })
        self.assertNotEqual(response.status_code, 200)
        login_url = reverse('login')
        self.assertTrue(response.url.startswith(login_url))
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.first_name, 'Unauthorized')
        self.assertNotEqual(self.user.last_name, 'Update')

    def test_user_delete(self):
        response = self.client.post(reverse('user_delete',
                                            kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(pk=self.user.pk)

    def test_user_delete_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse('user_delete',
                                            kwargs={'pk': self.user.pk}))
        self.assertNotEqual(response.status_code, 200)
        login_url = reverse('login')
        self.assertTrue(response.url.startswith(login_url))
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

    def test_user_update_different_user(self):
        other_user = User.objects.create_user(username='otheruser',
                                              password='otherpass')
        response = self.client.post(reverse('user_update',
                                            kwargs={'pk': other_user.pk}), {
                                        'first_name': 'Wrong',
                                        'last_name': 'User'
                                    })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users'))
        self.assertTrue(User.objects.filter(pk=other_user.pk).exists())

    def test_user_delete_different_user(self):
        other_user = User.objects.create_user(username='otheruser',
                                              password='otherpass')
        response = self.client.post(reverse('user_delete',
                                            kwargs={'pk': other_user.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users'))
        self.assertTrue(User.objects.filter(pk=other_user.pk).exists())
