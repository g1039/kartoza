"""Service layer for the core application."""

from typing import Any


def update_profile_details(
    *,
    user: Any,
    first_name: str,
    last_name: str,
    home_address: str,
    phone_number: str,
) -> None:
    """Update the provided user's profile details."""

    user.first_name = first_name
    user.last_name = last_name
    user.home_address = home_address
    user.phone_number = phone_number
    user.save()
