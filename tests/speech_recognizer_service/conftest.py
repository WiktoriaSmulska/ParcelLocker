from datetime import date
from unittest.mock import MagicMock

import pytest

from src.model import Delivers


@pytest.fixture
def deliver_11() -> Delivers:
    """
    Fixture for creating a delivery object.

    Returns:
        Delivers: A delivery for parcel '1' to locker '1' with specific sender/receiver emails and dates.
    """
    return Delivers(
        parcel_id="P12345",
        locker_id="12345",
        sender_email="bob.jones@gmail.com",
        receiver_email="jane.smith@example.com",
        sent_date=date(2023, 12, 2),
        expected_delivery_date=date(2023, 12, 6)
    )

@pytest.fixture
def deliver_22() -> Delivers:
    """
    Fixture for creating a delivery object.

    Returns:
        Delivers: A delivery for parcel '1' to locker '1' with a different sender/receiver email and dates.
    """
    return Delivers(
        parcel_id="1",
        locker_id="1",
        sender_email="alice.smith@gmail.com",
        receiver_email="john.doe@example.com",
        sent_date=date(2023, 12, 1),
        expected_delivery_date=date(2023, 12, 7)
    )
@pytest.fixture
def mock_deliver_repo(deliver_11: Delivers, deliver_22:Delivers):
    """
    Fixture for creating a mocked repository to return the delivery objects.

    This fixture mocks the `get_data` method of the repository to return a list of two predefined
    deliveries, `deliver_11` and `deliver_22`. This allows for testing how the service interacts
    with the repository without requiring actual data storage.

    Args:
        deliver_11 (Delivers): A sample delivery object for parcel 'P12345'.
        deliver_22 (Delivers): A sample delivery object for parcel '1'.

    Returns:
        MagicMock: A mocked repository that returns the list of delivery objects when `get_data` is called.
    """
    repo = MagicMock()
    repo.get_data.return_value = [deliver_11, deliver_22]
    return repo
