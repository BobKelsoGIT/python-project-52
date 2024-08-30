from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import User


class UserCRUDTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_user_create(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'first_name': 'John',
            'last_name': 'Doe'
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_update(self):
        response = self.client.post(reverse('user_update', kwargs={'pk': self.user.pk}), {
            'first_name': 'Updated',
            'last_name': 'Name'
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')

    def test_user_update_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse('user_update', kwargs={'pk': self.user.pk}), {
            'first_name': 'Unauthorized',
            'last_name': 'Update'
        })
        self.assertNotEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.first_name, 'Unauthorized')

    def test_user_delete(self):
        response = self.client.post(reverse('user_delete', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_user_delete_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse('user_delete', kwargs={'pk': self.user.pk}))
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

    def test_user_update_different_user(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        response = self.client.post(reverse('user_update', kwargs={'pk': other_user.pk}), {
            'first_name': 'Wrong',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 403)
        other_user.refresh_from_db()
        self.assertNotEqual(other_user.first_name, 'Wrong')

    def test_user_delete_different_user(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        response = self.client.post(reverse('user_delete', kwargs={'pk': other_user.pk}))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(User.objects.filter(pk=other_user.pk).exists())
