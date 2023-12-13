from django import forms
from .models import Mbs


class MbsForm(forms.ModelForm):
    class Meta:
        model = Mbs
        fields = ["content"]
