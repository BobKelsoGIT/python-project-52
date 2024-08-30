from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import User
from django.utils.translation import gettext_lazy as _
from .signup_form import CreateUserForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


class UsersListView(ListView):
    model = User
    template_name = 'users/users_list.html'
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


class UserUpdateView(UpdateView):
    pass


class UserDeleteView(DeleteView):
    pass
