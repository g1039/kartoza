from typing import Generator, Optional
from unittest.mock import Mock, patch

import pytest
from django.test import RequestFactory

from webapp.portfolio import messages
from webapp.portfolio.messages import get_extra_tags


@pytest.fixture
def mock_django_messages() -> Generator[Mock, None, None]:
    """Mock out the built in django messages."""

    with patch("webapp.portfolio.messages.django_messages") as mock:
        yield mock


@pytest.mark.parametrize("method", ["info", "debug", "warning", "error", "success"])
def test_messages_method_call(
    method: str, rf: RequestFactory, mock_django_messages: Mock
) -> None:
    """Ensure the messages are passed to the appropriate built in messages method."""

    message = "Testing"
    request = rf.get("some-url")
    getattr(messages, method)(request=request, message=message)

    expected_method = getattr(mock_django_messages, method)
    expected_method.assert_called_with(
        request=request, message=message, extra_tags=None
    )


@pytest.mark.parametrize(
    "auto_close_after_ms,expected_result",
    [(5000, "alert-close-5000"), (1000, "alert-close-1000"), (None, None)],
)
def test_get_extra_tags(
    auto_close_after_ms: Optional[int], expected_result: Optional[str]
) -> None:
    """Ensure get_extra_tags generates the appropriate tags for auto close."""
    actual_result = get_extra_tags(auto_close_after_ms=auto_close_after_ms)
    assert actual_result == expected_result


def test_messages_with_auto_close(
    rf: RequestFactory, mock_django_messages: Mock
) -> None:
    message = "Testing"
    request = rf.get("some-url")
    messages.info(request=request, message=message, auto_close_after_ms=1000)
    mock_django_messages.info.assert_called_with(
        request=request, message=message, extra_tags="alert-close-1000"
    )
