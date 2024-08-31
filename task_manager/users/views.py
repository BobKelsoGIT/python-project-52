from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import User
from django.utils.translation import gettext_lazy as _
from .signup_form import CreateUserForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages


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


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name']
    template_name = 'form.html'
    success_url = reverse_lazy('users')
    success_message = _('User successfully updated')
    extra_context = {
        'title': _('Update user'),
        'button_text': _('Update'),
    }

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user:
            raise PermissionDenied("You are not allowed to update this user.")
        return obj


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users')
    template_name = 'delete_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('users')
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user:
            raise PermissionDenied("You are not allowed to delete other users.")
        return obj

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied:
            messages.error(request, _('You are not allowed to delete other users.'))
            return redirect('users')