from pytest import FixtureRequest
from src.converter import UserConverter, ParcelConverter, LockerConverter, DeliversConverter

import pytest



@pytest.mark.parametrize("user_data_fixture_name, user_fixture_name", [
    ("user_1_data", "user_1"),
    ("user_2_data", "user_2")
])
def test_user_converter_from_json(user_data_fixture_name: str, user_fixture_name: str, request: FixtureRequest) -> None:
    """
    Tests the conversion of user data from JSON format to a User model instance.

    :param user_data_fixture_name: The fixture name containing user data in dictionary format.
    :param user_fixture_name: The fixture name containing the expected User model instance.
    :param request: Pytest request object to retrieve fixture values.
    """
    user = request.getfixturevalue(user_fixture_name)
    user_data = request.getfixturevalue(user_data_fixture_name)

    converter = UserConverter()
    data_expected = converter.convert(user_data)

    assert data_expected.email == user.email


@pytest.mark.parametrize("parcel_data_fixture_name, parcel_fixture_name", [
    ("parcel_1_data", "parcel_1"),
    ("parcel_2_data", "parcel_2")
])
def test_parcel_converter_from_json(parcel_data_fixture_name: str, parcel_fixture_name: str, request: FixtureRequest):
    """
    Tests the conversion of parcel data from JSON format to a Parcel model instance.

    :param parcel_data_fixture_name: The fixture name containing parcel data in dictionary format.
    :param parcel_fixture_name: The fixture name containing the expected Parcel model instance.
    :param request: Pytest request object to retrieve fixture values.
    """
    parcel = request.getfixturevalue(parcel_fixture_name)
    parcel_data = request.getfixturevalue(parcel_data_fixture_name)
    converter = ParcelConverter()
    result = converter.convert(parcel_data)

    assert result.parcel_id == parcel.parcel_id


@pytest.mark.parametrize("locker_data_fixture_name, locker_fixture_name", [
    ("locker_1_data", "locker_1"),
    ("locker_2_data", "locker_2")
])
def test_locker_converter_from_json(locker_data_fixture_name: str, locker_fixture_name: str, request: FixtureRequest):
    """
    Tests the conversion of locker data from JSON format to a Locker model instance.

    :param locker_data_fixture_name: The fixture name containing locker data in dictionary format.
    :param locker_fixture_name: The fixture name containing the expected Locker model instance.
    :param request: Pytest request object to retrieve fixture values.
    """
    locker = request.getfixturevalue(locker_fixture_name)
    locker_data = request.getfixturevalue(locker_data_fixture_name)
    converter = LockerConverter()
    result = converter.convert(locker_data)

    assert result.locker_id == locker.locker_id


@pytest.mark.parametrize("deliver_data_fixture_name, deliver_fixture_name", [
    ("deliver_1_data", "deliver_1"),
    ("deliver_2_data", "deliver_2")
])
def test_delivers_converter_from_json(deliver_data_fixture_name: str, deliver_fixture_name: str,
                                      request: FixtureRequest):
    """
    Tests the conversion of delivery data from JSON format to a Delivers model instance.

    :param deliver_data_fixture_name: The fixture name containing delivery data in dictionary format.
    :param deliver_fixture_name: The fixture name containing the expected Delivers model instance.
    :param request: Pytest request object to retrieve fixture values.
    """
    deliver = request.getfixturevalue(deliver_fixture_name)
    deliver_data = request.getfixturevalue(deliver_data_fixture_name)

    converter = DeliversConverter()
    result = converter.convert(deliver_data)

    assert result.sender_email == deliver.sender_email