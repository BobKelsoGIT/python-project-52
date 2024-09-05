from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _

from .models import User


class UserForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150, required=True, label=_("First name")
    )
    last_name = forms.CharField(
        max_length=150, required=True, label=_("Last name")
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(
                pk=self.instance.pk).exists():
            raise forms.ValidationError(
                _("A user with that username already exists."))
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', _("Passwords must match"))

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get("password1")

        if password1:
            user.set_password(password1)

        if commit:
            user.save()
        return user
