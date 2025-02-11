from src.model import (
    Delivers,
    Users,
    Parcels,
    Lockers,
    LockerComponentsSize,
    City,

    UserDataDict,
    ParcelsDataDict,
    LockersDataDict,
    DeliversDataDict
)


def test_user_to_dict(user_1: Users, user_1_data: UserDataDict):
    """
    Test conversion of a `Users` object to a dictionary.

    This ensures that the `to_dict()` method correctly converts
    a `Users` instance into its expected dictionary representation.
    """
    data = user_1.to_dict()
    assert data == user_1_data


def test_parcel_to_dict(parcel_1: Parcels, parcel_1_data: ParcelsDataDict):
    """
    Test conversion of a `Parcels` object to a dictionary.

    This verifies that the `to_dict()` method correctly translates
    a `Parcels` instance into the expected dictionary format.
    """
    data = parcel_1.to_dict()
    assert data == parcel_1_data


def test_locker_to_dict(locker_1: Lockers, locker_1_data: LockersDataDict):
    """
    Test conversion of a `Lockers` object to a dictionary.

    This ensures that the `to_dict()` method accurately represents
    a `Lockers` instance in dictionary form.
    """
    data = locker_1.to_dict()
    assert data == locker_1_data


def test_deliver_to_dict(deliver_1: Delivers, deliver_1_data: DeliversDataDict):
    """
    Test conversion of a `Delivers` object to a dictionary.

    This test ensures that the `to_dict()` method correctly
    transforms a `Delivers` instance into the expected dictionary format.
    """
    data = deliver_1.to_dict()
    assert data == deliver_1_data
