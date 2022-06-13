"""Log activity of sign in/out by using Django signal."""

from typing import Any

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.functions import Now
from django.dispatch import receiver
from django.http import HttpRequest

from webapp.portfolio.models import UserActivity


@receiver(user_logged_in)
def log_user_login(
    sender: HttpRequest, request: HttpRequest, user: Any, **kwargs: Any
) -> Any:
    """User login receiver."""

    UserActivity.objects.create(
        user=user,
    )


@receiver(user_logged_out)
def log_user_logout(
    sender: HttpRequest, request: HttpRequest, user: Any, **kwargs: Any
) -> Any:
    """User logout receiver."""

    UserActivity.objects.filter(
        user=user,
    ).update(logout=Now())
