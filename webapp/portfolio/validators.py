"""Validator classes for model field validation."""
import re
from typing import Any

from django.core.exceptions import ValidationError

REGEX_AREA_CODE_MOBILE = r"(^60[3-9])|(^63[0-7])|(^66[0-5])|(^68[0-5])|(^69[0-5])|(^61\d)|(^62\d)|(^64\d)|(^65\d)|(^67\d)|(^7[1-4]\d)|(^76\d)|(^7[8-9]\d)|(^81[0-8])|(^8[2-4]\d)"


def phone_number_validator(value: Any) -> None:
    """Validate phone number."""

    regex = r"^\+27[6-8]\d{8}$"
    area_code_mobile = value[3:6] if len(value) > 9 else ""

    if not re.search(regex, value) or not re.search(
        REGEX_AREA_CODE_MOBILE, area_code_mobile
    ):
        raise ValidationError(
            "Invalid phone number: Phone number must match this format +27607702214."
        )
