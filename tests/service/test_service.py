from unittest.mock import MagicMock, patch
from src.model import Delivers, Users, Parcels, Lockers, LockerComponentsSize, City
import logging

logging.basicConfig(level=logging.DEBUG)


def test_get_parcel_size(purchase_summary_service, parcel_11, parcel_22, parcel_33) -> None:
    """
    Test to verify the correct size classification for parcels based on their dimensions.

    Args:
        purchase_summary_service (PurchaseSummaryService): The service being tested.
        parcel_11 (Parcels): A small parcel.
        parcel_22 (Parcels): A medium parcel.
        parcel_33 (Parcels): A large parcel.

    Asserts:
        Verifies if the parcel size classification matches the expected values.
    """
    size_1 = purchase_summary_service.get_parcel_size(parcel_11)
    assert size_1 == LockerComponentsSize.SMALL, f"Expected 'small', but got {size_1}"

    size_2 = purchase_summary_service.get_parcel_size(parcel_22)
    assert size_2 == LockerComponentsSize.MEDIUM, f"Expected 'medium', but got {size_2}"

    size_3 = purchase_summary_service.get_parcel_size(parcel_33)
    assert size_3 == LockerComponentsSize.LARGE, f"Expected 'large', but got {size_3}"


def test_check_locker_capacity_no_exceed(purchase_summary_service, parcel_11, parcel_22, locker_11, locker_22,
                                         deliver_11, deliver_22) -> None:
    """
    Test to ensure that the locker capacity is not exceeded when deliveries are made.

    Args:
        purchase_summary_service (PurchaseSummaryService): The service being tested.
        parcel_11 (Parcels): A small parcel.
        parcel_22 (Parcels): A medium parcel.
        locker_11 (Lockers): A locker with available capacity.
        locker_22 (Lockers): Another locker with available capacity.
        deliver_11 (Delivers): A delivery object.
        deliver_22 (Delivers): A delivery object.

    Asserts:
        Verifies that no error is logged when the locker capacity is not exceeded.
    """
    with patch("logging.error") as mock_logging_error:
        purchase_summary_service.check_locker_capacity()
        mock_logging_error.assert_not_called()


def test_check_locker_capacity_exceed(purchase_summary_service, parcel_11, parcel_22, parcel_33, locker_11, locker_22,
                                      deliver_11, deliver_22, deliver_33) -> None:
    """
    Test to ensure that an error is logged when the locker capacity is exceeded.

    Args:
        purchase_summary_service (PurchaseSummaryService): The service being tested.
        parcel_11 (Parcels): A small parcel.
        parcel_22 (Parcels): A medium parcel.
        parcel_33 (Parcels): A large parcel.
        locker_11 (Lockers): A locker with a limited capacity.
        locker_22 (Lockers): Another locker.
        deliver_11 (Delivers): A delivery object.
        deliver_22 (Delivers): A delivery object.
        deliver_33 (Delivers): A delivery object.

    Asserts:
        Verifies that an error is logged when the capacity for small parcels is exceeded in locker '1'.
    """
    locker_11.compartments[LockerComponentsSize.SMALL] = 1
    purchase_summary_service.lockers = {"1": locker_11, "2": locker_22}
    purchase_summary_service.delivers = [deliver_11, deliver_22, deliver_33]

    with patch("logging.error") as mock_logging_error:
        purchase_summary_service.check_locker_capacity()
        mock_logging_error.assert_called_with(
            'Locker 1 exceeded capacity for LockerComponentsSize.SMALL parcels. Used: 2, Capacity: 1')


def test_most_often_used_size_of_parcel(purchase_summary_service, parcel_11, parcel_22, parcel_33, locker_11, locker_22,
                                        deliver_11, deliver_22, deliver_33) -> None:
    """
    Test to determine the most often used parcel sizes for each locker.

    Args:
        purchase_summary_service (PurchaseSummaryService): The service being tested.
        parcel_11 (Parcels): A small parcel.
        parcel_22 (Parcels): A medium parcel.
        parcel_33 (Parcels): A large parcel.
        locker_11 (Lockers): A locker object.
        locker_22 (Lockers): A locker object.
        deliver_11 (Delivers): A delivery object.
        deliver_22 (Delivers): A delivery object.
        deliver_33 (Delivers): A delivery object.

    Asserts:
        Verifies if the most popular sizes for each locker are identified correctly.
    """
    most_popular_sizes = purchase_summary_service.most_often_used_size_of_parcel()

    assert most_popular_sizes == {
        '1': [LockerComponentsSize.SMALL],
        '2': [LockerComponentsSize.MEDIUM]
    }


def test_person_who_sended_and_picked_up_packages(purchase_summary_service, deliver_11, deliver_22, deliver_33, user_1,
                                                  user_2) -> None:
    """
    Test to determine the persons who have sent and received the most packages, along with the farthest distance.

    Args:
        purchase_summary_service (PurchaseSummaryService): The service being tested.
        deliver_11 (Delivers): A delivery object.
        deliver_22 (Delivers): A delivery object.
        deliver_33 (Delivers): A delivery object.
        user_1 (Users): A user object (sender/receiver).
        user_2 (Users): A user object (sender/receiver).

    Asserts:
        Verifies that the expected users are identified as senders and receivers,
        and that the farthest distances are correctly calculated.
    """
    purchase_summary_service.users = {
        "bob.jones@gmail.com": user_1,
        "alice.smith@gmail.com": user_2,
        "jane.smith@example.com": user_1,
        "john.doe@example.com": user_2
    }

    farthest_senders, farthest_receivers = purchase_summary_service.person_who_sended_and_picked_up_packages(3)

    assert set(farthest_senders.keys()) == {"alice.smith@gmail.com", "bob.jones@gmail.com"}, \
        f"Expected senders to include ['alice.smith@gmail.com', 'bob.jones@gmail.com'], but got {farthest_senders.keys()}"
    assert set(farthest_receivers.keys()) == {"john.doe@example.com", "jane.smith@example.com"}, \
        f"Expected receivers to include ['john.doe@example.com', 'jane.smith@example.com'], but got {farthest_receivers.keys()}"

    assert farthest_senders["alice.smith@gmail.com"]["max_distance"] > 0, \
        "Expected a positive max_distance for 'alice.smith@gmail.com'"
    assert "farthest_locker" in farthest_senders["alice.smith@gmail.com"], \
        "Expected 'farthest_locker' key in sender details"


def test_longest_delivery(purchase_summary_service, deliver_11, deliver_22, deliver_33) -> None:
    """
    Test to determine the longest delivery time and the sender responsible for it.

    Args:
        purchase_summary_service (PurchaseSummaryService): The service being tested.
        deliver_11 (Delivers): A delivery object.
        deliver_22 (Delivers): A delivery object.
        deliver_33 (Delivers): A delivery object.

    Asserts:
        Verifies that the longest delivery time is correctly identified and the sender is correct.
    """
    max_sender, longest_time = purchase_summary_service.longest_delivery()

    assert max_sender == "alice.smith@gmail.com", \
        f"Expected 'alice.smith@gmail.com' as sender with the longest delivery, but got {max_sender}"
    assert longest_time == 10, \
        f"Expected 10 days as the longest delivery time, but got {longest_time}"
