from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "input is-primary"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "input is-primary"}),
    )
    next = forms.CharField(widget=forms.HiddenInput(), required=False)
