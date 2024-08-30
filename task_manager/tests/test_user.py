from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import User
from django.utils.translation import gettext as _
from django.contrib.messages import get_messages


class UserCRUDTest(TestCase):

    def setUp(self):
        # Создаем пользователя для тестов обновления и удаления
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_user_create(self):
        # Тест создания нового пользователя
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'first_name': 'John',
            'last_name': 'Doe'
        })

        # Проверка перенаправления на страницу входа (или другую страницу успеха)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        # Проверка создания пользователя
        self.assertTrue(User.objects.filter(username='newuser').exists())

        # Проверка сообщения об успехе
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == _('User successfully created') for message in messages))

    def test_user_update(self):
        # Тест обновления существующего пользователя
        response = self.client.post(reverse('user_update', kwargs={'pk': self.user.pk}), {
            'first_name': 'Updated',
            'last_name': 'Name'
        })
        self.assertEqual(response.status_code, 302)  # Проверка перенаправления
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')  # Проверка обновленного имени
        self.assertEqual(self.user.last_name, 'Name')  # Проверка обновленной фамилии

    def test_user_update_not_logged_in(self):
        # Тест обновления пользователя без входа в систему
        self.client.logout()
        response = self.client.post(reverse('user_update', kwargs={'pk': self.user.pk}), {
            'first_name': 'Unauthorized',
            'last_name': 'Update'
        })
        self.assertNotEqual(response.status_code, 200)  # Проверка, что запрос не прошел
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.first_name, 'Unauthorized')  # Имя пользователя не должно измениться

    def test_user_delete(self):
        # Тест удаления пользователя
        response = self.client.post(reverse('user_delete', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 302)  # Проверка перенаправления
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())  # Проверка, что пользователь удален

    def test_user_delete_not_logged_in(self):
        # Тест удаления пользователя без входа в систему
        self.client.logout()
        response = self.client.post(reverse('user_delete', kwargs={'pk': self.user.pk}))
        self.assertNotEqual(response.status_code, 200)  # Проверка, что запрос не прошел
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())  # Пользователь не должен быть удален

    def test_user_update_different_user(self):
        # Тест обновления другого пользователя
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        response = self.client.post(reverse('user_update', kwargs={'pk': other_user.pk}), {
            'first_name': 'Wrong',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 403)  # Проверка отказа в доступе
        other_user.refresh_from_db()
        self.assertNotEqual(other_user.first_name, 'Wrong')  # Имя пользователя не должно измениться

    def test_user_delete_different_user(self):
        # Тест удаления другого пользователя
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        response = self.client.post(reverse('user_delete', kwargs={'pk': other_user.pk}))
        self.assertEqual(response.status_code, 403)  # Проверка отказа в доступе
        self.assertTrue(User.objects.filter(pk=other_user.pk).exists())  # Пользователь не должен быть удален
