"""Form classes for the portfolio application."""

from typing import Any

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from webapp.portfolio.models import Reference

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form for use in the admin panel."""

    class Meta:
        model = User
        fields = ("email",)
        field_classes = {"email": forms.EmailField}

    def save(self, commit: bool = True) -> Any:
        """Generate a new user.

        This form is meant to be used with the django admin panel.
        """

        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = Reference.generate_username()

        if commit:
            user.save()
        return user
