from src.model import City, LockerComponentsSize
from datetime import date
import pytest


@pytest.fixture
def compartments_test_cases():
    """
    Fixture that provides test cases for locker compartment validation.

    This fixture returns various combinations of locker compartments with their expected validity.
    Each test case consists of a dictionary of compartment sizes and a boolean indicating whether
    the configuration is valid.

    Returns:
        list: A list of tuples where each tuple contains a dictionary of compartment sizes and a boolean.
    """
    return [
        ({LockerComponentsSize.SMALL: 1, LockerComponentsSize.MEDIUM: 2}, True),

        ({LockerComponentsSize.SMALL: -1, LockerComponentsSize.MEDIUM: 2}, False),

        ({LockerComponentsSize.SMALL: 0, LockerComponentsSize.MEDIUM: 2}, False),

        ({LockerComponentsSize.SMALL: 1, LockerComponentsSize.MEDIUM: "invalid"}, False),

        ({}, True),
    ]


@pytest.fixture
def parcels_test_cases():
    """
    Fixture that provides test cases for parcel validation.

    This fixture returns test cases to validate the dimensions and weight of parcels. Each test case
    consists of a dictionary representing the parcel's attributes and a boolean indicating whether
    the parcel's attributes are valid.

    Returns:
        list: A list of tuples where each tuple contains a dictionary of parcel attributes and a boolean.
    """
    return [
        ({"height": 10, "length": 20, "weight": 5}, True),

        ({"height": -10, "length": 20, "weight": 5}, False),

        ({"height": 10, "length": 0, "weight": 5}, False),

        ({"height": 10, "length": "invalid", "weight": 5}, False),

        ({"height": 10, "length": 20}, False),
    ]


@pytest.fixture
def delivers_test_cases():
    """
    Fixture that provides test cases for validating delivery data.

    This fixture returns test cases to validate the sender and receiver emails in delivery objects. Each test case
    consists of a dictionary with the sender and receiver emails and a boolean indicating whether the delivery
    data is valid.

    Returns:
        list: A list of tuples where each tuple contains a dictionary of delivery data and a boolean.
    """
    return [
        ({"sender_email": "test@example.com", "receiver_email": "test@example.com"}, False),

        ({"sender_email": "sender@example.com", "receiver_email": "receiver@example.com"}, True),

        ({"sender_email": "test@example.com"}, False),

        ({}, False),
    ]


@pytest.fixture
def dates_of_delivers():
    """
    Fixture that provides test cases for validating the send and expected delivery dates.

    This fixture returns test cases to check the validity of send and expected delivery dates in deliveries.
    Each test case consists of a dictionary with the send and expected delivery dates and a boolean indicating
    whether the dates are valid (send_date should not be later than expected_delivery_date).

    Returns:
        list: A list of tuples where each tuple contains a dictionary of dates and a boolean.
    """
    return [
        ({"send_date": date(2024, 12, 18), "expected_delivery_date": date(2024, 12, 19)}, True),

        ({"send_date": date(2024, 12, 19), "expected_delivery_date": date(2024, 12, 18)}, False),

        ({"send_date": date(2024, 12, 19), "expected_delivery_date": date(2024, 12, 19)}, True),

        ({"send_date": date(2024, 12, 19)}, False),

        ({}, False),

        ({"send_date": "invalid_date", "expected_delivery_date": date(2024, 12, 19)}, False),
    ]
