"""Wrapper on the builtin django messages that adds theme specific options."""

from typing import Optional

from django.contrib import messages as django_messages
from django.http import HttpRequest


def get_extra_tags(*, auto_close_after_ms: Optional[int] = None) -> Optional[str]:
    """Return the extra tags given the provided inputs."""

    if auto_close_after_ms is None:
        return None

    return f"alert-close-{auto_close_after_ms}"


def debug(
    *, request: HttpRequest, message: str, auto_close_after_ms: Optional[int] = None
) -> None:
    """Create a debug message."""

    django_messages.debug(
        request=request,
        message=message,
        extra_tags=get_extra_tags(auto_close_after_ms=auto_close_after_ms),
    )


def info(
    *, request: HttpRequest, message: str, auto_close_after_ms: Optional[int] = None
) -> None:
    """Create a info message."""

    django_messages.info(
        request=request,
        message=message,
        extra_tags=get_extra_tags(auto_close_after_ms=auto_close_after_ms),
    )


def warning(
    *, request: HttpRequest, message: str, auto_close_after_ms: Optional[int] = None
) -> None:
    """Create a warning message."""

    django_messages.warning(
        request=request,
        message=message,
        extra_tags=get_extra_tags(auto_close_after_ms=auto_close_after_ms),
    )


def error(
    *, request: HttpRequest, message: str, auto_close_after_ms: Optional[int] = None
) -> None:
    """Create a error message."""

    django_messages.error(
        request=request,
        message=message,
        extra_tags=get_extra_tags(auto_close_after_ms=auto_close_after_ms),
    )


def success(
    *, request: HttpRequest, message: str, auto_close_after_ms: Optional[int] = None
) -> None:
    """Create a success message."""

    django_messages.success(
        request=request,
        message=message,
        extra_tags=get_extra_tags(auto_close_after_ms=auto_close_after_ms),
    )
