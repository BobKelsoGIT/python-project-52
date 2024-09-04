from django import forms
from .models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Label.objects.filter(name=name).exclude(
                id=self.instance.id).exists():
            raise forms.ValidationError('Метка с таким именем уже существует.')
        return name
