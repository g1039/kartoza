import pytest

from webapp.portfolio.factories import CustomUserFactory
from webapp.portfolio.models import Reference


def test_custom_user_str_() -> None:
    instance = CustomUserFactory.build()
    assert str(instance) == instance.username


@pytest.mark.parametrize(
    "first_name,last_name,expected_result",
    [
        ("Foo", "Bob", "Foo Bob"),
        ("Foo", "", "Foo"),
    ],
)
def test_full_name(first_name: str, last_name: str, expected_result: str) -> None:
    instance = CustomUserFactory.build(first_name=first_name, last_name=last_name)
    assert instance.get_full_name() == expected_result


def test_custom_user_get_short_name() -> None:
    instance = CustomUserFactory.build()
    assert instance.get_short_name() == instance.first_name


@pytest.mark.django_db
def test_reference_generate_username() -> None:
    username = Reference.generate_username()
    assert isinstance(username, str)
    assert username.startswith("user-")
