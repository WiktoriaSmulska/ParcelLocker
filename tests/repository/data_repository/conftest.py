import pytest
from unittest.mock import MagicMock
from src.repository import (
    UserDataRepository,
    ParcelDataRepository,
    LockerDataRepository,
    DeliverDataRepository
)

@pytest.fixture
def file_reader_mock() -> MagicMock:
    """
    Creates a mock object for file reading operations.
    """
    return MagicMock()

@pytest.fixture
def validator_mock() -> MagicMock:
    """
    Creates a mock object for data validation operations.
    """
    return MagicMock()

@pytest.fixture
def converter_mock() -> MagicMock:
    """
    Creates a mock object for data conversion operations.
    """
    return MagicMock()

@pytest.fixture
def user_data_repository(
        file_reader_mock: MagicMock,
        validator_mock: MagicMock,
        converter_mock: MagicMock
) -> UserDataRepository:
    """
    Provides a UserDataRepository instance with mocked dependencies.
    """
    return UserDataRepository(
        file_reader=file_reader_mock,
        validator=validator_mock,
        converter=converter_mock,
        filename='users.json'
    )

@pytest.fixture
def parcel_data_repository(
        file_reader_mock: MagicMock,
        validator_mock: MagicMock,
        converter_mock: MagicMock
) -> ParcelDataRepository:
    """
    Provides a ParcelDataRepository instance with mocked dependencies.
    """
    return ParcelDataRepository(
        file_reader=file_reader_mock,
        validator=validator_mock,
        converter=converter_mock,
        filename='parcels.json'
    )

@pytest.fixture
def locker_data_repository(
        file_reader_mock: MagicMock,
        validator_mock: MagicMock,
        converter_mock: MagicMock
) -> LockerDataRepository:
    """
    Provides a LockerDataRepository instance with mocked dependencies.
    """
    return LockerDataRepository(
        file_reader=file_reader_mock,
        validator=validator_mock,
        converter=converter_mock,
        filename='lockers.json'
    )

@pytest.fixture
def deliver_data_repository(
        file_reader_mock: MagicMock,
        validator_mock: MagicMock,
        converter_mock: MagicMock
) -> DeliverDataRepository:
    """
    Provides a DeliverDataRepository instance with mocked dependencies.
    """
    return DeliverDataRepository(
        file_reader=file_reader_mock,
        validator=validator_mock,
        converter=converter_mock,
        filename='delivers.json'
    )