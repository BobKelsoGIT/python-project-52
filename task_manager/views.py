from django.views.generic.base import TemplateView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'form.html'
    next_page = reverse_lazy('home')
    success_message = _('Logged in successfully!')
    extra_context = {
        'title': _('Log in1'),
        'button_text': _('Log in'),
    }


class UserLogoutView(SuccessMessageMixin, LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
