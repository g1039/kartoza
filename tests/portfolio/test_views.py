from http import HTTPStatus
from unittest.mock import Mock, patch

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import Client, RequestFactory
from django.urls import reverse

from webapp.portfolio.factories import CustomUserFactory
from webapp.portfolio.views import ProfileDetailView, home_view, logout_view

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


class TestProfileDetailView:
    def test_get_initial(self, rf: RequestFactory) -> None:
        user = CustomUserFactory.build()
        request = rf.get("some-url")
        request.user = user
        view = ProfileDetailView(request=request)
        expected_result = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "home_address": user.home_address,
            "phone_number": user.phone_number,
        }
        actual_result = view.get_initial()
        assert actual_result == expected_result

    @pytest.mark.django_db
    def test_get_is_editable(self, rf: RequestFactory) -> None:
        request = rf.get("some-url")
        request.user = CustomUserFactory(is_active=True)
        view = ProfileDetailView(request=request)
        response = view.get_is_editable()
        assert type(response) == bool

    @pytest.mark.django_db
    def test_form_valid(self, rf: RequestFactory) -> None:
        user = CustomUserFactory(
            is_active=True, last_name="Zuckerberg", phone_number="+27639920376"
        )
        request = rf.get("some-url")
        form = Mock()
        form.cleaned_data = {
            "first_name": user.first_name,
            "last_name": "Jones",
            "home_address": user.home_address,
            "phone_number": "+27812638653",
        }
        request.user = user

        view = ProfileDetailView(request=request)

        with patch("webapp.portfolio.views.messages"):
            response = view.form_valid(form)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse("profile-detail")
