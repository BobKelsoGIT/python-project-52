from django import forms

from .models import Status


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Status.objects.filter(name=name).exclude(
                id=self.instance.id).exists():
            raise forms.ValidationError('Статус с таким именем уже существует.')
        return name
