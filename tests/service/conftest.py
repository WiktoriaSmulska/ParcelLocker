from datetime import date
from unittest.mock import MagicMock
from src.repository import (
    UserDataRepository,
    ParcelDataRepository,
    LockerDataRepository,
    DeliverDataRepository,
    PurchaseSummaryRepository
)
from src.service import PurchaseSummaryService
from tests.conftest import user_1
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
def parcel_11():
    """
    Fixture for creating a parcel object with specific attributes.

    Returns:
        Parcels: A parcel with id '1', height 5, length 10, and weight 3.
    """
    return Parcels(parcel_id="1", height=5, length=10, weight=3)

@pytest.fixture
def parcel_22():
    """
    Fixture for creating a parcel object with specific attributes.

    Returns:
        Parcels: A parcel with id '2', height 25, length 40, and weight 3.
    """
    return Parcels(parcel_id="2", height=25, length=40, weight=3)

@pytest.fixture
def parcel_33():
    """
    Fixture for creating a parcel object with specific attributes.

    Returns:
        Parcels: A parcel with id '3', height 35, length 60, and weight 3.
    """
    return Parcels(parcel_id="3", height=35, length=60, weight=3)


@pytest.fixture
def locker_11() -> Lockers:
    """
    Fixture for creating a locker object with specific city and compartments.

    Returns:
        Lockers: A locker in Los Angeles with a mix of small, medium, and large compartments.
    """
    return Lockers(
        locker_id="1",
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
def locker_22() -> Lockers:
    """
    Fixture for creating a locker object with specific city and compartments.

    Returns:
        Lockers: A locker in Los Angeles with a different mix of small, medium, and large compartments.
    """
    return Lockers(
        locker_id="2",
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
def locker_33() -> Lockers:
    """
    Fixture for creating another locker object with similar attributes as locker_11.

    Returns:
        Lockers: Another locker in Los Angeles with a similar configuration as locker_11.
    """
    return Lockers(
        locker_id="3",
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
def deliver_11() -> Delivers:
    """
    Fixture for creating a delivery object.

    Returns:
        Delivers: A delivery for parcel '1' to locker '1' with specific sender/receiver emails and dates.
    """
    return Delivers(
        parcel_id="1",
        locker_id="1",
        sender_email="bob.jones@gmail.com",
        receiver_email="jane.smith@example.com",
        sent_date=date(2023, 12, 2),
        expected_delivery_date=date(2023, 12, 6)
    )

@pytest.fixture
def deliver_22() -> Delivers:
    """
    Fixture for creating a delivery object.

    Returns:
        Delivers: A delivery for parcel '1' to locker '1' with a different sender/receiver email and dates.
    """
    return Delivers(
        parcel_id="1",
        locker_id="1",
        sender_email="alice.smith@gmail.com",
        receiver_email="john.doe@example.com",
        sent_date=date(2023, 12, 1),
        expected_delivery_date=date(2023, 12, 7)
    )

@pytest.fixture
def deliver_33() -> Delivers:
    """
    Fixture for creating a delivery object.

    Returns:
        Delivers: A delivery for parcel '2' to locker '2' with specific sender/receiver emails and dates.
    """
    return Delivers(
        parcel_id="2",
        locker_id="2",
        sender_email="alice.smith@gmail.com",
        receiver_email="john.doe@example.com",
        sent_date=date(2023, 12, 3),
        expected_delivery_date=date(2023, 12, 13)
    )

@pytest.fixture
def mock_user_repo(user_1: Users, user_2: Users) -> MagicMock:
    """
    Fixture for mocking the user repository.

    Args:
        user_1 (Users): A user object.
        user_2 (Users): A user object.

    Returns:
        MagicMock: A mock repository for users.
    """
    repo = MagicMock()
    repo.get_data.return_value = [user_1, user_2]
    return repo


@pytest.fixture
def mock_parcel_repo(parcel_11: Parcels, parcel_22: Parcels) -> MagicMock:
    """
    Fixture for mocking the parcel repository.

    Args:
        parcel_11 (Parcels): A parcel object.
        parcel_22 (Parcels): A parcel object.

    Returns:
        MagicMock: A mock repository for parcels.
    """
    repo = MagicMock()
    repo.get_data.return_value = [parcel_11, parcel_22]
    return repo


@pytest.fixture
def mock_locker_repo(locker_11: Lockers, locker_22: Lockers) -> MagicMock:
    """
    Fixture for mocking the locker repository.

    Args:
        locker_11 (Lockers): A locker object.
        locker_22 (Lockers): A locker object.

    Returns:
        MagicMock: A mock repository for lockers.
    """
    repo = MagicMock()
    repo.get_data.return_value = [locker_11, locker_22]
    return repo


@pytest.fixture
def mock_deliver_repo(deliver_11: Delivers, deliver_22: Delivers, deliver_33: Delivers) -> MagicMock:
    """
    Fixture for mocking the delivery repository.

    Args:
        deliver_11 (Delivers): A delivery object.
        deliver_22 (Delivers): A delivery object.
        deliver_33 (Delivers): A delivery object.

    Returns:
        MagicMock: A mock repository for deliveries.
    """
    repo = MagicMock()
    repo.get_data.return_value = [deliver_11, deliver_22, deliver_33]
    return repo


@pytest.fixture
def purchase_summary_service(
        mock_user_repo: UserDataRepository,
        mock_parcel_repo:ParcelDataRepository,
        mock_locker_repo: LockerDataRepository,
        mock_deliver_repo: DeliverDataRepository,
        user_1: Users,
        user_2: Users,
        parcel_11: Parcels,
        parcel_22: Parcels,
        locker_11: Lockers,
        locker_22: Lockers,
        deliver_11: Delivers,
        deliver_22: Delivers,
        deliver_33: Delivers,
) -> PurchaseSummaryService:
    """
    Fixture for initializing the PurchaseSummaryService with mocked repositories and test data.

    Args:
        mock_user_repo (UserDataRepository): Mocked user repository.
        mock_parcel_repo (ParcelDataRepository): Mocked parcel repository.
        mock_locker_repo (LockerDataRepository): Mocked locker repository.
        mock_deliver_repo (DeliverDataRepository): Mocked delivery repository.
        user_1 (Users): A user object.
        user_2 (Users): A user object.
        parcel_11 (Parcels): A parcel object.
        parcel_22 (Parcels): A parcel object.
        locker_11 (Lockers): A locker object.
        locker_22 (Lockers): A locker object.
        deliver_11 (Delivers): A delivery object.
        deliver_22 (Delivers): A delivery object.
        deliver_33 (Delivers): A delivery object.

    Returns:
        PurchaseSummaryService: An instance of the PurchaseSummaryService with the provided data.
    """
    return PurchaseSummaryService(
        user_repo=mock_user_repo,
        parcel_repo=mock_parcel_repo,
        locker_repo=mock_locker_repo,
        deliver_repo=mock_deliver_repo,
        lockers = {locker_11.locker_id: locker_11, locker_22.locker_id: locker_22},
        parcels = {parcel_11.parcel_id: parcel_11, parcel_22.parcel_id: parcel_22},
        delivers = [deliver_11, deliver_22, deliver_33],
        users = {user_1.email: user_1, user_2.email: user_2},
        locker_usage={locker.locker_id: {'small': 0, 'medium': 0, 'large': 0} for locker in [locker_11, locker_22]}
    )
