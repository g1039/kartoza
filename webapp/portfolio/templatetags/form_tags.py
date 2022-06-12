"""Custom template tags for working with forms."""

from typing import Any
from urllib.parse import urlencode

from django import template

register = template.Library()


@register.filter
def encode_query_dict(value: Any) -> str:
    """Convert the provided query dict to a query string."""

    return urlencode(value)
