from django.views.generic.base import TemplateView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'form.html'
    next_page = reverse_lazy('home')
    success_message = _('Logged in successfully!')
    extra_context = {
        'title': _('Log in'),
        'button_text': _('Login'),
    }


class UserLogoutView(SuccessMessageMixin, LogoutView):
    next_page = reverse_lazy('home')
    success_message = _('Logged out successfully!')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('Logged out successfully!'))
        return super().dispatch(request, *args, **kwargs)
