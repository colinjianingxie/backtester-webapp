from django import forms
from django.contrib.auth.forms import UserCreationForm

from oauth.models.user_model import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=100, help_text="Required. Add a valid email address"
    )

    class Meta:
        model = Account  # Will need the required fields from the Account model
        fields = ("email", "username", "password1", "password2")
