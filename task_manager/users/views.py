from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import User
from .signup_form import CreateUserForm
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from task_manager.mixins import UserPermissionMixin
from django.contrib.messages.views import SuccessMessageMixin


class UsersListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'
    extra_context = {
        'title': _('Users')
    }


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CreateUserForm
    template_name = 'form.html'
    success_url = reverse_lazy('login')
    success_message = _('User successfully created')
    extra_context = {
        'title': _('Create user'),
        'button_text': _('Create'),
    }


class UserUpdateView(UserPermissionMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name']
    template_name = 'form.html'
    success_url = reverse_lazy('users')
    success_message = _('User successfully updated')
    extra_context = {
        'title': _('Update user'),
        'button_text': _('Update'),
    }


class UserDeleteView(UserPermissionMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users')
    template_name = 'delete_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('users')
        return context
