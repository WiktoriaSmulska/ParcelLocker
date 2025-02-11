from datetime import date
from unittest.mock import MagicMock
from src.repository import (
    UserDataRepository,
    ParcelDataRepository,
    LockerDataRepository,
    DeliverDataRepository
)
from src.model import (
    LockerComponentsSize,
    Users,
    City,
    Lockers,
    Parcels,
    Delivers,
UserDataDict,
LockersDataDict,
ParcelsDataDict,
DeliversDataDict

)
from pathlib import Path
from src.file_service import UserJsonFileReader
from src.converter import  UserConverter
from src.validator import UserDataDictValidator
import logging
import pytest
import json

from tests.conftest import parcel_1, user_1_data


def test_get_data_empty_cache_logs_warning(
        user_data_repository: UserDataRepository,
        caplog: pytest.LogCaptureFixture) -> None:
    """
    Tests whether a warning is logged when trying to get data from an empty cache.

    Args:
        user_data_repository (UserDataRepository): The repository instance.
        caplog (pytest.LogCaptureFixture): Captures log output for verification.

    Asserts:
        - The log contains a warning about an empty cache.
        - The returned data list is empty.
    """
    with caplog.at_level(logging.WARNING):
        data = user_data_repository.get_data()
        assert "No data available in cache" in caplog.text
        assert len(data) == 0

def test_refresh_user_data_calls_file_reader_and_process_data(
    user_data_repository: UserDataRepository,
        file_reader_mock: MagicMock,
        user_1: Users,
        user_1_data: UserDataDict
) -> None:

    """
    Tests whether `refresh_data` correctly calls the file reader and processes user data.

    Args:
        user_data_repository (UserDataRepository): The repository instance.
        file_reader_mock (MagicMock): Mocked file reader.
        user_1 (Users): Example user object.
        user_1_data (UserDataDict): Dictionary representation of `user_1`.

    Asserts:
        - The file reader is called with 'users.json'.
        - The data contains exactly one user.
        - The retrieved user attributes match the expected values.
    """

    file_reader_mock.read.return_value = [user_1_data]

    user_data_repository.validator.validate.return_value = True # type: ignore[attr-defined]
    user_data_repository.converter.convert.return_value = user_1 # type: ignore[attr-defined]


    data = user_data_repository.refresh_data()

    file_reader_mock.read.assert_called_with('users.json')
    assert file_reader_mock.read.call_count == 2
    assert len(data) == 1
    assert data[0].email == "bob.jones@gmail.com"
    assert data[0].name == "Bob"
    assert data[0].surname == "Jones"
    assert data[0].city == City.NEW_YORK
    assert data[0].latitude == 37.774929
    assert data[0].longitude == -122.419418


def test_refresh_parcel_data_calls_file_reader_and_process_data(
    parcel_data_repository: ParcelDataRepository,
        file_reader_mock: MagicMock,
        parcel_1: Parcels,
        parcel_1_data: ParcelsDataDict
) -> None:

    """
    Tests whether `refresh_data` correctly processes parcel data.

    Args:
        parcel_data_repository (ParcelDataRepository): The repository instance.
        file_reader_mock (MagicMock): Mocked file reader.
        parcel_1 (Parcels): Example parcel object.
        parcel_1_data (ParcelsDataDict): Dictionary representation of `parcel_1`.

    Asserts:
        - The file reader is called with 'parcels.json'.
        - The retrieved data matches the expected parcel attributes.
    """
    file_reader_mock.read.return_value = [parcel_1_data]
    parcel_data_repository.validator.validate.return_value = True # type: ignore[attr-defined]
    parcel_data_repository.converter.convert.return_value = parcel_1 # type: ignore[attr-defined]


    data = parcel_data_repository.refresh_data()

    file_reader_mock.read.assert_called_with('parcels.json')
    assert file_reader_mock.read.call_count == 2
    assert len(data) == 1
    assert data[0].parcel_id == "P67890"
    assert data[0].height == 20
    assert data[0].length == 40
    assert data[0].weight == 3


def test_refresh_locker_data_calls_file_reader_and_process_data(
    locker_data_repository: LockerDataRepository,
        file_reader_mock: MagicMock,
        locker_1: Lockers,
        locker_1_data: LockersDataDict
) -> None:

    """
    Tests whether `refresh_data` correctly processes locker data.

    Args:
        locker_data_repository (LockerDataRepository): The repository instance.
        file_reader_mock (MagicMock): Mocked file reader.
        locker_1 (Lockers): Example locker object.
        locker_1_data (LockersDataDict): Dictionary representation of `locker_1`.

    Asserts:
        - The file reader is called with 'lockers.json'.
        - The retrieved data matches the expected locker attributes.
    """
    file_reader_mock.read.return_value = [locker_1_data]
    locker_data_repository.validator.validate.return_value = True  # type: ignore[attr-defined]
    locker_data_repository.converter.convert.return_value = locker_1 # type: ignore[attr-defined]


    data = locker_data_repository.refresh_data()

    file_reader_mock.read.assert_called_with('lockers.json')
    assert file_reader_mock.read.call_count == 2
    assert len(data) == 1
    assert data[0].locker_id == "L002"
    assert data[0].city == City.LOS_ANGELES
    assert data[0].latitude == 34.052235
    assert data[0].longitude == -118.243683
    assert data[0].compartments[LockerComponentsSize.SMALL] == 25
    assert data[0].compartments[LockerComponentsSize.MEDIUM] == 10
    assert data[0].compartments[LockerComponentsSize.LARGE] == 8

def test_refresh_deliver_data_calls_file_reader_and_process_data(
    deliver_data_repository: DeliverDataRepository,
        file_reader_mock: MagicMock,
        deliver_1: Delivers,
        deliver_1_data
) -> None:

    """
    Tests that refresh_data() in DeliverDataRepository correctly reads and processes delivery data.

    This test ensures that:
    - The file reader is called to read from 'delivers.json'.
    - The validator and converter process the data correctly.
    - The returned data matches the expected deliver entry.

    Args:
        deliver_data_repository (DeliverDataRepository): The repository instance being tested.
        file_reader_mock (MagicMock): Mocked file reader service.
        deliver_1 (Delivers): A sample delivery instance for verification.
        deliver_1_data (dict): The raw data representation of a delivery.

    Assertions:
        - The file reader's read method is called with 'delivers.json'.
        - The read method is called exactly twice.
        - The repository returns exactly one delivery entry.
        - The returned delivery entry contains expected values.
    """
    file_reader_mock.read.return_value = [deliver_1_data]
    deliver_data_repository.validator.validate.return_value = True  # type: ignore[attr-defined]
    deliver_data_repository.converter.convert.return_value = deliver_1 # type: ignore[attr-defined]


    data = deliver_data_repository.refresh_data()

    file_reader_mock.read.assert_called_with('delivers.json')
    assert file_reader_mock.read.call_count == 2
    assert len(data) == 1
    assert data[0].parcel_id == "P67890"
    assert data[0].locker_id == "L002"
    assert data[0].sender_email == "bob.jones@gmail.com"
    assert data[0].receiver_email == "jane.smith@example.com"
    assert data[0].sent_date == date(2023, 12, 2)
    assert data[0].expected_delivery_date == date(2023, 12, 6)

def test_invalid_entry_logs_error(
        user_data_repository: UserDataRepository,
        file_reader_mock: MagicMock,
        validator_mock: MagicMock,
        caplog: pytest.LogCaptureFixture
) -> None:

    """
    Tests whether an invalid entry logs an error message.

    Args:
        user_data_repository (UserDataRepository): The repository instance.
        file_reader_mock (MagicMock): Mocked file reader.
        validator_mock (MagicMock): Mocked validator.
        caplog (pytest.LogCaptureFixture): Captures log output for verification.

    Asserts:
        - The error log contains the expected message.
        - The data list contains only the valid entry.
    """

    file_reader_mock.read.return_value = [
        {
            "id": 1,
            "email": "bob.jones@gmail.com",
            "name": "Bob",
            "surname": "Jones",
            "city": "San Francisco",
            "latitude": 37.774929,
            "longitude": -122.419418
        },
        {
            "id": 1,
            "email": "bob.jones@gmail.com",
            "name": "Bob",
            "surname": "Jones",
            "longitude": -122.419418
        }
    ]
    validator_mock.validate.side_effect = [True, False]

    with caplog.at_level(logging.ERROR):
        data = user_data_repository.refresh_data()

    invalid_entry = {
        "id": 1,
        "email": "bob.jones@gmail.com",
        "name": "Bob",
        "surname": "Jones",
        "longitude": -122.419418
    }
    expected_log_message = f"Invalid entry: {repr(invalid_entry)}"

    assert expected_log_message in caplog.text
    assert len(data) == 1

def test_no_filename_raises_value_error(
        file_reader_mock: MagicMock,
        validator_mock: MagicMock,
        converter_mock: MagicMock
)-> None:
    """
    Tests that an error is raised when attempting to create a repository without a filename.

    Args:
        file_reader_mock (MagicMock): Mocked file reader.
        validator_mock (MagicMock): Mocked validator.
        converter_mock (MagicMock): Mocked converter.

    Asserts:
        - A `ValueError` is raised with the expected message.
    """
    with pytest.raises(ValueError, match='No filename set'):
        user_data_repository = UserDataRepository(
            file_reader=file_reader_mock,
            validator=validator_mock,
            converter=converter_mock,
            filename=None
        )