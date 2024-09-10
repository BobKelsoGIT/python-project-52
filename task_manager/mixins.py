from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView


class BaseFormView(LoginRequiredMixin, SuccessMessageMixin):
    permission_denied_message = _('You are not logged in! Please log in.')
    template_name = 'components/form.html'

    def get_success_url(self):
        return reverse_lazy(self.success_url_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


class BaseCreateView(BaseFormView, CreateView):
    pass


class BaseUpdateView(BaseFormView, UpdateView):
    pass


class AuthRequiredMixin(LoginRequiredMixin):
    message = _('You are not logged in! Please log in.')
    ordering = ['pk']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.message)
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)


class BaseListView(AuthRequiredMixin, ListView):
    pass


class DeleteProtectionMixin:
    protected_message = None
    protected_url = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)


class BaseDeleteView(LoginRequiredMixin, DeleteProtectionMixin,
                     SuccessMessageMixin, DeleteView):
    template_name = 'components/delete_form.html'

    def get_success_url(self):
        return reverse_lazy(self.success_url_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


class UserPermissionMixin(UserPassesTestMixin):
    permission_message = None
    permission_url = None

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)


class AuthorDeletionMixin(UserPassesTestMixin):
    author_message = None
    author_url = None

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.author_message)
        return redirect(self.author_url)
