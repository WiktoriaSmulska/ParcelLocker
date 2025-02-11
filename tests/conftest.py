from datetime import date
from src.model import (
    LockerComponentsSize,
    Users,
    City,
    Lockers,
    Parcels,
    Delivers, UserDataDict, ParcelsDataDict, LockersDataDict, DeliversDataDict
)
import pytest

@pytest.fixture
def user_1() -> Users:
    """
    Fixture to create and return a user object for testing.

    Returns:
        Users: A User object representing 'Bob Jones'.
    """
    return Users(
        email="bob.jones@gmail.com",
        name="Bob",
        surname="Jones",
        city=City.NEW_YORK,
        latitude=37.774929,
        longitude=-122.419418
    )

@pytest.fixture
def user_1_data() -> UserDataDict:
    """
    Fixture to create and return a dictionary representing user 'Bob Jones' data.

    Returns:
        dict: A dictionary with 'Bob Jones' user data.
    """
    return {
        "email": "bob.jones@gmail.com",
        "name": "Bob",
        "surname": "Jones",
        "city": "New York",
        "latitude": 37.774929,
        "longitude": -122.419418
    }

@pytest.fixture
def user_2() -> Users:
    """
    Fixture to create and return a user object for testing.

    Returns:
        Users: A User object representing 'Alice Smith'.
    """
    return Users(
        email="alice.smith@gmail.com",
        name="Alice",
        surname="Smith",
        city=City.CHICAGO,
        latitude=41.878113,
        longitude=-87.629799
    )

@pytest.fixture
def user_2_data() -> UserDataDict:
    """
    Fixture to create and return a dictionary representing user 'Alice Smith' data.

    Returns:
        dict: A dictionary with 'Alice Smith' user data.
    """
    return {
        "email": "alice.smith@gmail.com",
        "name": "Alice",
        "surname": "Smith",
        "city": "Chicago",
        "latitude": 41.878113,
        "longitude": -87.629799
    }

@pytest.fixture
def parcel_1() -> Parcels:
    """
    Fixture to create and return a parcel object for testing.

    Returns:
        Parcels: A Parcel object with specific dimensions and weight.
    """
    return Parcels(
        parcel_id="P67890",
        height=20,
        length=40,
        weight=3
    )

@pytest.fixture
def parcel_2() -> Parcels:
    """
    Fixture to create and return another parcel object for testing.

    Returns:
        Parcels: A second Parcel object with specific dimensions and weight.
    """
    return Parcels(
        parcel_id="P12345",
        height=15,
        length=30,
        weight=2
    )

@pytest.fixture
def parcel_1_data() -> dict:
    """
    Fixture to create and return a dictionary representing the data for 'parcel_1'.

    Returns:
        dict: A dictionary with data for 'parcel_1'.
    """
    return {
        "parcel_id": "P67890",
        "height": 20,
        "length": 40,
        "weight": 3
    }

@pytest.fixture
def parcel_2_data() -> dict:
    """
    Fixture to create and return a dictionary representing the data for 'parcel_2'.

    Returns:
        dict: A dictionary with data for 'parcel_2'.
    """
    return {
        "parcel_id": "P12345",
        "height": 15,
        "length": 30,
        "weight": 2
    }

@pytest.fixture
def locker_1() -> Lockers:
    """
    Fixture to create and return a locker object for testing.

    Returns:
        Lockers: A Locker object with compartments of various sizes.
    """
    return Lockers(
        locker_id="L002",
        city=City.LOS_ANGELES,
        latitude=34.052235,
        longitude=-118.243683,
        compartments={
            LockerComponentsSize.SMALL: 25,
            LockerComponentsSize.MEDIUM: 10,
            LockerComponentsSize.LARGE: 8,
        }
    )

@pytest.fixture
def locker_2() -> Lockers:
    """
    Fixture to create and return another locker object for testing.

    Returns:
        Lockers: A second Locker object with compartments of various sizes.
    """
    return Lockers(
        locker_id="L003",
        city=City.LOS_ANGELES,
        latitude=47.606209,
        longitude=-122.332069,
        compartments={
            LockerComponentsSize.SMALL: 20,
            LockerComponentsSize.MEDIUM: 15,
            LockerComponentsSize.LARGE: 5,
        }
    )

@pytest.fixture
def locker_1_data() -> dict:
    """
    Fixture to create and return a dictionary representing the data for 'locker_1'.

    Returns:
        dict: A dictionary with data for 'locker_1'.
    """
    return {
        "locker_id": "L002",
        "city": "Los Angeles",
        "latitude": 34.052235,
        "longitude": -118.243683,
        "compartments": {
            'small': 25,
            "medium": 10,
            "large": 8,
        }
    }

@pytest.fixture
def locker_2_data() -> dict:
    """
    Fixture to create and return a dictionary representing the data for 'locker_2'.

    Returns:
        dict: A dictionary with data for 'locker_2'.
    """
    return {
        "locker_id": "L003",
        "city": "Los Angeles",
        "latitude": 47.606209,
        "longitude": -122.332069,
        "compartments": {
            'small': 20,
            "medium": 15,
            "large": 5,
        }
    }

@pytest.fixture
def deliver_1() -> Delivers:
    """
    Fixture to create and return a delivery object for testing.

    Returns:
        Delivers: A Delivery object representing a parcel delivery.
    """
    return Delivers(
        parcel_id="P67890",
        locker_id="L002",
        sender_email="bob.jones@gmail.com",
        receiver_email="jane.smith@example.com",
        sent_date=date(2023, 12, 2),
        expected_delivery_date=date(2023, 12, 6)
    )

@pytest.fixture
def deliver_2() -> Delivers:
    """
    Fixture to create and return another delivery object for testing.

    Returns:
        Delivers: A second Delivery object representing another parcel delivery.
    """
    return Delivers(
        parcel_id="P12345",
        locker_id="L003",
        sender_email="alice.smith@gmail.com",
        receiver_email="john.doe@example.com",
        sent_date=date(2023, 12, 3),
        expected_delivery_date=date(2023, 12, 7)
    )

@pytest.fixture
def deliver_1_data() -> dict:
    """
    Fixture to create and return a dictionary representing the data for 'deliver_1'.

    Returns:
        dict: A dictionary with data for 'deliver_1'.
    """
    return {
        "parcel_id": "P67890",
        "locker_id": "L002",
        "sender_email": "bob.jones@gmail.com",
        "receiver_email": "jane.smith@example.com",
        "sent_date": date(2023, 12, 2),
        "expected_delivery_date": date(2023, 12, 6)
    }

@pytest.fixture
def deliver_2_data() -> dict:
    """
    Fixture to create and return a dictionary representing the data for 'deliver_2'.

    Returns:
        dict: A dictionary with data for 'deliver_2'.
    """
    return {
        "parcel_id": "P12345",
        "locker_id": "L003",
        "sender_email": "alice.smith@gmail.com",
        "receiver_email": "john.doe@example.com",
        "sent_date": date(2023, 12, 3),
        "expected_delivery_date": date(2023, 12, 7)
    }
