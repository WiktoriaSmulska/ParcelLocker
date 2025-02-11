from src.file_service import (
    UserJsonFileReader,
    ParcelJsonFileReader,
    LockerJsonFileReader,
    DeliverJsonFileReader,
    UserJsonFileWriter,
    ParcelJsonFileWriter,
    LockerJsonFileWriter,
    DeliverJsonFileWriter
)
from src.model import UserDataDict, LockersDataDict, DeliversDataDict, ParcelsDataDict, Lockers, Delivers, Parcels

import os
import json

def test_read_user(user_file: str, user_data: list[UserDataDict]) -> None:
    """
    Test reading user data from a JSON file.
    """
    reader = UserJsonFileReader()
    users = reader.read(user_file)
    assert users == user_data

def test_read_parcel(parcel_file: str, parcel_data: list[ParcelsDataDict]) -> None:
    """
    Test reading parcel data from a JSON file.
    """
    reader = ParcelJsonFileReader()
    users = reader.read(parcel_file)
    assert users == parcel_data

def test_read_locker(locker_file: str, locker_data: list[LockersDataDict]) -> None:
    """
    Test reading locker data from a JSON file.
    """
    reader = LockerJsonFileReader()
    users = reader.read(locker_file)
    assert users == locker_data

def test_read_deliver(deliver_file: str, deliver_data: list[DeliversDataDict]) -> None:
    """
    Test reading delivery data from a JSON file.
    """
    reader = DeliverJsonFileReader()
    users = reader.read(deliver_file)
    assert users == deliver_data

def test_writer_user(tmpdir, user_data: list[UserDataDict]) -> None:
    """
    Test writing user data to a JSON file and verifying its contents.
    """
    writer = UserJsonFileWriter()
    file_path = os.path.join(tmpdir, 'test_user.json')
    writer.write(file_path, user_data)

    with open(file_path, 'r', encoding='utf8') as file:
        saved_data = json.load(file)

    assert saved_data == user_data
