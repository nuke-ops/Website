from django import forms
from .models import validate_name


class DiceForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"id": "name", "class": "input is-primary", "placeholder": "Name"}
        ),
        validators=[validate_name],
    )
    dice = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "id": "dice",
                "class": "input is-primary",
                "placeholder": "Dice",
                "value": 1,
                "step": "any",
            }
        ),
    )
    sides = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "id": "sides",
                "class": "input is-primary",
                "placeholder": "Sides",
                "value": 20,
                "step": "any",
            }
        ),
    )
    modifier = forms.CharField(required=False)
    raw_modifier = forms.CharField(required=False)
