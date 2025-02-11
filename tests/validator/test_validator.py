from enum import Enum
from src.validator import AbstractValidator
from typing import Type
from datetime import date
from src.validator import UserDataDictValidator, LockerDataDictValidator, ParcelDataDictValidator, \
    DeliverDataDictValidator
from src.model import UserDataDict, ParcelsDataDict, LockersDataDict, DeliversDataDict, LockerComponentsSize, Users, \
    City

import pytest



@pytest.mark.parametrize("value, expected", [
    (5, True),
    (-5, False),
    (0, False),
    ("10.5", True),
    ("-10.5", False),
    ("abc", False),
    ("", False)
])
def test_is_positive(value: int, expected: bool) -> None:
    """
    Test the `is_positive` method from AbstractValidator to verify if a value is positive.
    Validates positive integers, zero, negative numbers, and non-numeric values.

    Args:
        value: The value to test.
        expected: The expected result (True if value is positive, otherwise False).
    """
    assert AbstractValidator.is_positive(value) == expected


@pytest.mark.parametrize("value, enum_class, expected", [
    ("New York", City, True),
    ("Los Angeles", City, True),
    ('NEW YORK', City, False),
    ("large", LockerComponentsSize, True),
    ("big", LockerComponentsSize, False),
    ("small", LockerComponentsSize, True),
])
def test_is_valid_value_of(value: str, enum_class: Type[Enum], expected: bool) -> None:
    """
    Test the `is_valid_value_of` method from AbstractValidator to verify if a string matches a valid enum value.
    Ensures case sensitivity is respected for enum values.

    Args:
        value: The string to test.
        enum_class: The Enum class to check against (e.g., City or LockerComponentsSize).
        expected: The expected result (True if valid enum value, False otherwise).
    """
    assert AbstractValidator.is_valid_value_of(value, enum_class) == expected


@pytest.mark.parametrize("email, expected", [
    ("valid@gmail.com", True),
    ("invalid-email.com", False),
    ("@missingusername.com", False),
    ("missingdomain@", False),
    ("user@nonexistentdomain.invalid", False)
])
def test_is_valid_email(email: str, expected: bool) -> None:
    """
    Test the `is_valid_email` method from AbstractValidator to validate email addresses.
    Checks for common email format issues such as missing '@', missing domain, etc.

    Args:
        email: The email to validate.
        expected: The expected result (True if valid email, False otherwise).
    """
    assert AbstractValidator.is_valid_email(email) == expected


@pytest.mark.parametrize("value, pattern, expected", [
    ("abc123", r"[a-z]+\d+", True),
    ("123abc", r"[a-z]+\d+", False)
])
def test_validate_string_with_regex(value: str, pattern: str, expected: bool) -> None:
    """
    Test the `validate_string_with_regex` method from AbstractValidator to validate strings with regular expressions.
    Ensures the string matches the specified regex pattern.

    Args:
        value: The string to validate.
        pattern: The regex pattern to check against.
        expected: The expected result (True if string matches the regex, False otherwise).
    """
    assert AbstractValidator.validate_string_with_regex(value, pattern) == expected


def test_are_compartments_non_negative(compartments_test_cases) -> None:
    """
    Test the `are_compartments_non_negative` method from AbstractValidator to ensure that compartments values are non-negative.
    This test verifies different test cases for valid and invalid compartments configurations.

    Args:
        compartments_test_cases: A fixture containing test cases of compartments and their expected validity.
    """
    for compartments, expected in compartments_test_cases:
        result = AbstractValidator.are_compartments_non_negative(compartments)
        assert result == expected, f"Failed for compartments: {compartments}"


def test_are_sizes_bigger_than_zero(parcels_test_cases) -> None:
    """
    Test the `are_sizes_bigger_than_zero` method from AbstractValidator to verify that parcel sizes (height, length, weight) are positive.
    Ensures that parcels with zero or negative values are flagged as invalid.

    Args:
        parcels_test_cases: A fixture containing test cases of parcels and their expected validity.
    """
    for parcel, expected in parcels_test_cases:
        result = AbstractValidator.are_sizes_bigger_than_zero(parcel)
        assert result == expected, f"Failed for parcel: {parcel}"


def test_check_where_packed_is_send(delivers_test_cases) -> None:
    """
    Test the `check_to_who_packed_is_send` method from AbstractValidator to ensure that the sender and receiver are different.
    Verifies that deliveries where the sender and receiver are the same are flagged as invalid.

    Args:
        delivers_test_cases: A fixture containing test cases of deliveries and their expected validity.
    """
    for deliver, expected in delivers_test_cases:
        result = AbstractValidator.check_to_who_packed_is_send(deliver)
        assert result == expected, f"Failed for deliver: {deliver}"


def test_dates_of_delivery(dates_of_delivers) -> None:
    """
    Test the `check_if_dates_of_delivery_are_different` method from AbstractValidator to validate the send and expected delivery dates.
    Ensures that the send date is not later than the expected delivery date.

    Args:
        dates_of_delivers: A fixture containing test cases with send and expected delivery dates.
    """
    for deliver, expected in dates_of_delivers:
        result = AbstractValidator.check_if_dates_of_delivery_are_different(deliver)
        assert result == expected, f"Failed for deliver: {deliver}"


@pytest.mark.parametrize("data, expected", [
    ({"email": "john.doe@gmail.com", "name": "John", "surname": "Doe", "city": "New York", "latitude": 40.712776,
      "longitude": -74.005974}, True),
    ({"email": "john.doe@@@example.com", "name": "John", "surname": "Doe", "city": "Los Angeles", "latitude": 34.052235,
      "longitude": -118.243683}, False),
    ({"email": 1, "name": "Invalid", "surname": "User", "city": "Invalid City", "latitude": 0.0, "longitude": 0.0},
     False),
    ({"email": "alice.smith@gmail.com", "name": "Alice", "surname": "Smith", "city": "Chicago", "latitude": 41.878113,
      "longitude": -87.629799}, True),
])
def test_user_data_dict_validator(data: UserDataDict, expected: bool) -> None:
    """
    Test the `UserDataDictValidator` class to validate user data dictionaries.
    Ensures that user data meets specific criteria (valid email, city, etc.) and is complete.

    Args:
        data: The user data to validate.
        expected: The expected result (True if valid user data, False otherwise).
    """
    validator = UserDataDictValidator()
    assert validator.validate(data) == expected


@pytest.mark.parametrize("data, expected", [
    ({"email": "john.doe@gmail.com", "name": "John", "surname": "Doe", "city": "New York", "latitude": 40.712776},
     False),
    ({"email": "john.doe@@@example.com", "surname": "Doe", "city": "Los Angeles", "latitude": 34.052235,
      "longitude": -118.243683}, False),
])
def test_user_data_dict_validator_missing_keys(data: UserDataDict, expected: bool) -> None:
    """
    Test the `UserDataDictValidator` class for user data dictionaries that are missing required keys.
    Ensures that missing essential fields (e.g., email, name) result in invalid data.

    Args:
        data: The user data to validate.
        expected: The expected result (True if data is invalid due to missing keys).
    """
    validator = UserDataDictValidator()
    assert validator.validate(data) == expected


@pytest.mark.parametrize("data, expected", [
    ({"height": 30, "length": 50, "weight": 5}, True),
    ({"height": 0, "length": -5, "weight": -5}, False),
    ({"height": 0, "length": 0, "weight": 0}, False),
])
def test_parcel_data_dict_validator(data: ParcelsDataDict, expected: bool) -> None:
    """
    Test the `ParcelDataDictValidator` to validate parcel data dictionaries.
    Ensures that parcels have valid dimensions (height, length, weight) greater than zero.

    Args:
        data: The parcel data to validate.
        expected: The expected result (True if parcel data is valid, False otherwise).
    """
    validator = ParcelDataDictValidator(["height", "length", "weight"])
    assert validator.validate(data) == expected


@pytest.mark.parametrize("data, expected", [
    ({"height": 20, "length": 40, "weight": 3}, False),
    ({"parcel_id": "P67890", "height": 20, "length": 40}, False),
])
def test_parcel_data_dict_validator_missing_keys(data: ParcelsDataDict, expected: bool) -> None:
    """
    Test the `ParcelDataDictValidator` for missing keys in the parcel data.
    Ensures that missing essential keys (e.g., parcel_id, weight) result in invalid data.

    Args:
        data: The parcel data to validate.
        expected: The expected result (True if invalid due to missing keys).
    """
    validator = ParcelDataDictValidator()
    assert validator.validate(data) == expected


@pytest.mark.parametrize("data, expected", [
    ({"locker_id": "L12345", "latitude": 52.2297, "longitude": 21.0122}, False),
    ({"locker_id": "L67890", "city": "Warsaw", "latitude": 52.2297, "longitude": 21.0122, "compartments": {}}, False),
    ({"locker_id": "L12345", "city": "Warsaw", "latitude": 52.2297, "longitude": 21.0122,
      "compartments": {"small": 5, "medium": 10, "large": 2}}, False),
])
def test_locker_data_dict_validator_missing_keys(data: LockersDataDict, expected: bool) -> None:
    """
    Test the `LockerDataDictValidator` class for locker data dictionaries that are missing essential keys.
    Ensures that incomplete data (missing compartments, locker_id, etc.) results in invalid lockers.

    Args:
        data: The locker data to validate.
        expected: The expected result (True if locker data is invalid due to missing keys).
    """
    validator = LockerDataDictValidator()
    assert validator.validate(data) == expected


@pytest.mark.parametrize("data, expected", [
    ({"parcel_id": "P67890", "locker_id": "L002", "sender_email": "bob.jones@example.com",
      "sent_date": date(2023, 12, 2), "expected_delivery_date": date(2023, 12, 6)}, False),
    ({"parcel_id": "P67890", "locker_id": "L002", "sender_email": "bob.jones@example.com",
      "receiver_email": "invalid-email", "sent_date": date(2023, 12, 2), "expected_delivery_date": date(2023, 12, 6)},
     True),
])
def test_deliver_data_dict_validator_missing_keys(data: DeliversDataDict, expected: bool) -> None:
    """
    Test the `DeliverDataDictValidator` class for delivery data that is missing essential keys.
    Ensures invalid data is detected when key fields such as emails or delivery dates are incorrect or missing.

    Args:
        data: The delivery data to validate.
        expected: The expected result (True if invalid due to missing or incorrect keys).
    """
    validator = DeliverDataDictValidator()
    assert validator.validate(data) == expected


@pytest.mark.parametrize("data, expected", [
    ({"city": "New York"}, True),
    ({"city": "Los Angeles"}, True),
    ({"city": "NEW YORK"}, False),
    ({"city": "Chicago"}, True),
    ({"city": "Boston"}, False),
])
def test_locker_data_dict_validator(data: LockersDataDict, expected: bool) -> None:
    """
    Test the `LockerDataDictValidator` to validate locker data dictionaries.
    Ensures that locker data with cities meets the expected city names.

    Args:
        data: The locker data to validate.
        expected: The expected result (True if city is valid, False otherwise).
    """
    validator = LockerDataDictValidator(["city"])
    assert validator.validate(data) == expected


@pytest.mark.parametrize("data, expected", [
    ({"sender_email": "alice.smith@example.com", "receiver_email": "alice.smith@example.com"}, True),
    ({"sender_email": "alice.smith@example.com", "receiver_email": "john.doe@example.com"}, False),
    ({"sender_email": "alice.smith@example.com", "receiver_email": "alice.smith@example.com"}, True),
])
def test_deliver_data_dict_validator(data: DeliversDataDict, expected: bool) -> None:
    """
    Test the `DeliverDataDictValidator` to check if the sender and receiver emails match.
    Verifies that a parcel can't be delivered to the same person (sender and receiver should be different).

    Args:
        data: The deliver data to validate.
        expected: The expected result (True if sender and receiver emails match).
    """
    validator = DeliverDataDictValidator(["sender_email", "receiver_email"])
    assert validator.validate(data) != expected
