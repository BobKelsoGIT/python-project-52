from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from task_manager.mixins import AuthRequiredMixin, UserPermissionMixin

from .forms import UserForm

User = get_user_model()


class UsersListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'
    extra_context = {
        'title': _('Users')
    }


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'form.html'
    success_url = reverse_lazy('login')
    success_message = _('User successfully created')
    extra_context = {
        'title': _('Create user'),
        'button_text': _('Register'),
    }


class UserUpdateView(AuthRequiredMixin, UserPermissionMixin,
                     SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'form.html'
    success_url = reverse_lazy('users')
    success_message = _('User successfully updated')
    permission_url = reverse_lazy('users')
    permission_message = _('You have no rights to change another user.')
    extra_context = {
        'title': _('Update user'),
        'button_text': _('Update'),
    }


class UserDeleteView(AuthRequiredMixin, UserPermissionMixin,
                     SuccessMessageMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users')
    template_name = 'delete_form.html'
    success_message = _('User is successfully deleted')
    permission_message = _('You have no rights to change another user.')
    permission_url = reverse_lazy('users')
    extra_context = {
        'cancel_url': reverse_lazy('users')
    }
