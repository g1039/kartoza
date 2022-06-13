import pytest
from django.core.exceptions import ValidationError

from webapp.portfolio.validators import phone_number_validator


@pytest.mark.parametrize(
    "value",
    [
        "+27363363222",
        "0611230101",
        "+28232323232",
        "+27999999991",
        "+27879999991",
    ],
)
def test_mobile_validator(value: str) -> None:
    with pytest.raises(ValidationError):
        phone_number_validator(value)
