from django import forms

from .models import Providers


class ProvidersForm(forms.ModelForm):
    class Meta:
        model = Providers
        fields = '__all__'
