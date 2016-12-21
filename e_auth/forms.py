from django import forms
from django.contrib.auth.models import User

# form for user creation


class UserCreation(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Username'}), max_length=30, min_length=3)
    # , validators=[isValidUsername, validators.validate_slug])
    email = forms.EmailField(label="", widget=forms.EmailInput(
        attrs={'placeholder': 'Email'}), max_length=100, error_messages={'invalid': ("Invalid Email.")})
    # , validators=[isValidEmail])
    password1 = forms.CharField(label="", max_length=50, min_length=6, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ("username", 'password', 'email')


