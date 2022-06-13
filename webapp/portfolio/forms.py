"""Form classes for the portfolio application."""

from typing import Any

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from webapp.portfolio.models import CustomUser, Reference
from webapp.portfolio.validators import phone_number_validator

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


class ProfileDetailsForm(forms.Form):
    """Read only form with user profile details."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Instantiate the form instance."""

        self.user = kwargs.pop("user", None)
        super(ProfileDetailsForm, self).__init__(*args, **kwargs)

    first_name = forms.CharField(
        help_text="Your first name.",
        disabled=False,
        required=True,
    )
    last_name = forms.CharField(
        help_text="Your last name.",
        disabled=False,
        required=True,
    )
    email = forms.EmailField(
        help_text="Your email address.",
        disabled=True,
        required=False,
    )

    home_address = forms.CharField(
        help_text="Your home address.",
        disabled=False,
        required=False,
    )

    phone_number = forms.CharField(
        help_text="Your phone number.",
        disabled=False,
        required=True,
        validators=[phone_number_validator],
    )

    def clean_phone_number(self) -> str:
        """Provide the provided phone number."""

        phone_number = self.cleaned_data["phone_number"]

        if (
            CustomUser.objects.filter(phone_number=phone_number)
            .exclude(username=self.user)
            .exists()
        ):
            self.add_error(
                "phone_number", "A user with that phone number already exists."
            )

        return phone_number
