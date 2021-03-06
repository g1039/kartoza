from unittest.mock import patch

import pytest
from django.contrib.auth.forms import AuthenticationForm

from webapp.portfolio.factories import CustomUserFactory
from webapp.portfolio.forms import CustomUserCreationForm, ProfileDetailsForm


@pytest.mark.django_db
def test_custom_user_creation_form() -> None:
    with patch(
        "webapp.portfolio.forms.Reference.generate_username"
    ) as mock_generate_username:
        mock_generate_username.return_value = "user-1"
        form = CustomUserCreationForm(
            {
                "email": "testing@mail.com",
                "password1": "@Mypassword123",
                "password2": "@Mypassword123",
            }
        )
        form.is_valid()
        user = form.save()
        assert user.username == "user-1"


@pytest.mark.django_db
def test_email_is_unique() -> None:
    user = CustomUserFactory(email="foo@mail.com")
    form = CustomUserCreationForm(
        data={
            "email": user.email,
            "password": "@Mypassword123",
        }
    )
    errors = form.errors["email"]
    assert errors[0] == "A user with that email address already exists."


class TestLoginForm:
    @pytest.mark.django_db
    def test_valid(self) -> None:
        CustomUserFactory(email="foo@mail.com", password="@Mypassword123")
        form = AuthenticationForm(
            data={
                "username": "foo@mail.com",
                "password": "@Mypassword123",
            }
        )
        assert form.is_valid() is True

    @pytest.mark.django_db
    def test_invalid_wrong_email(self) -> None:
        CustomUserFactory(email="foo@mail.com", password="@Mypassword123")
        form = AuthenticationForm(
            data={
                "username": "bob@mail.com",
                "password": "@Mypassword123",
            }
        )

        assert form.is_valid() is False
        assert len(form.errors) == 1

    @pytest.mark.django_db
    def test_invalid_user_not_found(self) -> None:
        CustomUserFactory(password="@Mypassword123")
        form = AuthenticationForm(
            data={
                "username": "bobmartin@mail.com",
                "password": "@Mypassword123",
            }
        )

        assert form.is_valid() is False
        assert len(form.errors) == 1
        assert form.errors == {
            "__all__": [
                "Please enter a correct username and password. Note that both fields may be case-sensitive."
            ]
        }

    @pytest.mark.django_db
    def test_invalid_no_email(self) -> None:
        CustomUserFactory(password="@Mypassword123")
        form = AuthenticationForm(
            data={
                "username": "",
                "password": "",
            }
        )

        assert form.is_valid() is False
        assert len(form.errors) == 2
        assert form.errors["username"] == ["This field is required."]
        assert form.errors["password"] == ["This field is required."]


class TestProfileDetailsForm:
    @pytest.mark.django_db
    def test_phone_number_is_unique_positive(self) -> None:
        user = CustomUserFactory(email="foo@mail.com", phone_number="+27817702215")
        form = ProfileDetailsForm(
            user=user,
            data={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "home_address": user.home_address,
                "phone_number": user.phone_number,
            },
        )
        print(form)
        assert form.is_valid()

    @pytest.mark.django_db
    def test_phone_number_is_unique(self) -> None:
        user = CustomUserFactory(email="foo@mail.com", phone_number="+27817702214")
        form = ProfileDetailsForm(
            user=CustomUserFactory.build(),
            data={
                "phone_number": user.phone_number,
            },
        )

        errors = form.errors["phone_number"]
        assert errors[0] == "A user with that phone number already exists."
