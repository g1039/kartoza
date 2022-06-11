from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import Client, RequestFactory
from django.urls import reverse

from webapp.portfolio.factories import CustomUserFactory
from webapp.portfolio.views import home_view, logout_view

User = get_user_model()


class TestLoginView:
    @pytest.mark.django_db
    def test_get(self, client: Client) -> None:
        response = client.get(reverse("login"))

        assert response.status_code == HTTPStatus.OK

    @pytest.mark.django_db
    def test_post(self, client: Client) -> None:
        user = CustomUserFactory(is_active=True)
        url = reverse(
            "login",
        )
        response = client.post(
            url,
            {
                "username": user.email,
                "password": user.password,
            },
        )
        assert response.status_code == HTTPStatus.OK


class TestLogoutView:
    @pytest.mark.parametrize("verb", ["get", "options", "put", "patch", "trace"])
    def test_logout_view_invalid_method(self, rf: RequestFactory, verb: str) -> None:
        """UNit test to ensure authenticated users cannot access logout without a POST."""
        user = CustomUserFactory.build(is_active=True)
        method = getattr(rf, verb)
        request = method(reverse("logout"))
        request.user = user
        response = logout_view(request)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    @pytest.mark.django_db
    def test_logout_view_post(self, client: Client) -> None:
        """Integration test to ensure a user can logout."""
        user = CustomUserFactory(is_active=True)
        client.force_login(user)
        response = client.post(reverse("logout"))
        assert response.status_code == HTTPStatus.FOUND


@pytest.fixture
def test_home_view(rf: RequestFactory, anonymous_user: AnonymousUser) -> None:
    """Ensure an unathenticated user cannot access the login view."""

    request = rf.get("some-url")
    request.user = anonymous_user
    response = home_view(request=request)
    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db
def test_signup_view(client: Client) -> None:
    """Integration test for the signup view."""

    payload = {
        "email": "foo@mail.com",
        "password1": "@Mypassword123",
        "password2": "@Mypassword123",
    }
    url = reverse("signup")
    response = client.post(url, data=payload)
    user = User.objects.first()

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse("login")
    assert user.email == "foo@mail.com"
