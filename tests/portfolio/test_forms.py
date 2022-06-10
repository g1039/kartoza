from unittest.mock import patch

import pytest

from webapp.portfolio.forms import CustomUserCreationForm


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
