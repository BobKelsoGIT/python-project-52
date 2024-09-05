from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import User


class UserCRUDTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser',
                                            password='testpass')

    def setUp(self):
        self.client.login(username='testuser', password='testpass')

    def test_user_list_view(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')
        self.assertContains(response, self.user.username)

    def test_user_create(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'first_name': 'Joe',
            'last_name': 'Byden'
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'anotherpassword',
            'password2': 'anotherpassword',
            'first_name': 'John',
            'last_name': 'Doe'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)

    def test_user_update(self):
        response = self.client.post(
            reverse('user_update', kwargs={'pk': self.user.pk}), {
                'first_name': 'Updated',
                'last_name': 'Name',
                'username': self.user.username,
                'password1': 'newpassword123',
                'password2': 'newpassword123',
            })
        self.assertEqual(response.status_code, 302)
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
