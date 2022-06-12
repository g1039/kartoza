import pytest

from webapp.portfolio import services
from webapp.portfolio.factories import CustomUserFactory


@pytest.mark.django_db
def test_update_profile_details() -> None:
    """Ensure the profile details are updated."""

    user = CustomUserFactory(
        first_name="Ntu2ko",
        last_name="Dhlamini",
        home_address="1534 Hoog St, Petit, Gauteng, 1512",
        phone_number="+27830000000",
    )
    services.update_profile_details(
        user=user,
        first_name="Ntuthuko",
        last_name="Dlamini",
        home_address="1996 Cheriton Dr, Scottburgh, KwaZulu-Natal, 4182",
        phone_number="+27810123456",
    )

    user.refresh_from_db()
    assert user.first_name == "Ntuthuko"
    assert user.last_name == "Dlamini"
    assert user.home_address == "1996 Cheriton Dr, Scottburgh, KwaZulu-Natal, 4182"
    assert user.phone_number == "+27810123456"
