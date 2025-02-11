from src.model import UserDataDict, LockersDataDict, DeliversDataDict, ParcelsDataDict
import pytest
import os
import json

@pytest.fixture
def user_data(user_1_data: UserDataDict, user_2_data: UserDataDict) -> list[UserDataDict]:
    """Fixture that returns a list of user data dictionaries."""
    return [user_1_data, user_2_data]

@pytest.fixture
def locker_data(locker_1_data: LockersDataDict, locker_2_data: LockersDataDict) -> list[LockersDataDict]:
    """Fixture that returns a list of locker data dictionaries."""
    return [locker_1_data, locker_2_data]

@pytest.fixture
def deliver_data(deliver_1_data: DeliversDataDict, deliver_2_data: DeliversDataDict) -> list[DeliversDataDict]:
    """Fixture that returns a list of delivery data dictionaries. Currently empty."""
    return []

@pytest.fixture
def parcel_data(parcel_1_data: ParcelsDataDict, parcel_2_data: ParcelsDataDict) -> list[ParcelsDataDict]:
    """Fixture that returns a list of parcel data dictionaries."""
    return [parcel_1_data, parcel_2_data]

@pytest.fixture
def user_file(tmpdir, user_data: list[UserDataDict]) -> str:
    """Creates a temporary JSON file containing user data and returns the file path."""
    file_path = os.path.join(tmpdir, 'test_users.json')
    with open(file_path, 'w') as file:
        json.dump(user_data, file)
    return file_path

@pytest.fixture
def parcel_file(tmpdir, parcel_data: list[ParcelsDataDict]) -> str:
    """Creates a temporary JSON file containing parcel data and returns the file path."""
    file_path = os.path.join(tmpdir, 'test_parcels.json')
    with open(file_path, 'w') as file:
        json.dump(parcel_data, file)
    return file_path

@pytest.fixture
def locker_file(tmpdir, locker_data: list[LockersDataDict]) -> str:
    """Creates a temporary JSON file containing locker data and returns the file path."""
    file_path = os.path.join(tmpdir, 'test_lockers.json')
    with open(file_path, 'w') as file:
        json.dump(locker_data, file)
    return file_path

@pytest.fixture
def deliver_file(tmpdir, deliver_data: list[DeliversDataDict]) -> str:
    """Creates a temporary JSON file containing delivery data and returns the file path."""
    file_path = os.path.join(tmpdir, 'test_delivers.json')
    with open(file_path, 'w') as file:
        json.dump(deliver_data, file)
    return file_path
