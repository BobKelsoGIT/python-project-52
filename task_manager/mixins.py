from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin


class UserPermissionMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(self.request, _('Log in please!'))
        return redirect('login')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user:
            raise PermissionDenied("You are not allowed to access this user.")
        return obj

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied:
            messages.error(request,
                           _('You are not allowed to perform this action.'))
            return redirect('users')
