"""Factories for the porfolio application."""

import random
from typing import Any

from factory import PostGenerationMethodCall, Sequence, faker, lazy_attribute
from factory.django import DjangoModelFactory

from webapp.portfolio.models import CustomUser


def generate_random_phone_number() -> str:
    """Return a random phone number."""

    lb = int(1e8)
    ub = int(1e9) - 1
    number = str(random.randint(lb, ub))
    part_2 = number[2:5]
    part_3 = number[5:]
    return f"+2781{part_2}{part_3}"


class CustomUserFactory(DjangoModelFactory):
    """Generate custom user instance for testing."""

    class Meta:
        model = CustomUser
        django_get_or_create = ("username",)

    username = Sequence(lambda n: f"user-{n}")
    first_name = faker.Faker("first_name")
    last_name = faker.Faker("last_name")
    email = faker.Faker("email")
    home_address = faker.Faker("street_address")
    password = PostGenerationMethodCall("set_password", "password")
    is_staff = False
    is_active = True
    is_superuser = False

    @classmethod
    def admin_user(cls, commit: bool = False, **extra: Any) -> Any:
        """Create an admin user.

        If commit is True the record will be persisted to the database.
        """

        kwargs = {
            **extra,
            "is_superuser": True,
            "is_staff": True,
            "is_active": True,
        }

        if commit is True:
            return cls(**kwargs)
        else:
            return cls.build(**kwargs)

    @lazy_attribute
    def phone_number(self) -> str:
        """Generate a phone number."""

        return generate_random_phone_number()
