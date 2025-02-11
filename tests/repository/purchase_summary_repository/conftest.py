from datetime import date
from unittest.mock import MagicMock
from src.repository import (
    UserDataRepository,
    ParcelDataRepository,
    LockerDataRepository,
    DeliverDataRepository,
    PurchaseSummaryRepository
)
from src.model import (
    LockerComponentsSize,
    Users,
    City,
    Lockers,
    Parcels,
    Delivers,
    UserDataDict,
    ParcelsDataDict,
    LockersDataDict,
    DeliversDataDict
)
import pytest


@pytest.fixture
def mock_user_repo(user_1: Users, user_2: Users) -> MagicMock:
    """
    Creates a mock UserDataRepository that returns a predefined list of users.

    Args:
        user_1 (Users): A mock user instance.
        user_2 (Users): Another mock user instance.

    Returns:
        MagicMock: A mock repository with a predefined return value for get_data().
    """
    repo = MagicMock()
    repo.get_data.return_value = [user_1, user_2]
    return repo


@pytest.fixture
def mock_parcel_repo(parcel_1: Parcels, parcel_2: Parcels) -> MagicMock:
    """
    Creates a mock ParcelDataRepository that returns a predefined list of parcels.

    Args:
        parcel_1 (Parcels): A mock parcel instance.
        parcel_2 (Parcels): Another mock parcel instance.

    Returns:
        MagicMock: A mock repository with a predefined return value for get_data().
    """
    repo = MagicMock()
    repo.get_data.return_value = [parcel_1, parcel_2]
    return repo


@pytest.fixture
def mock_locker_repo(locker_1: Lockers, locker_2: Lockers) -> MagicMock:
    """
    Creates a mock LockerDataRepository that returns a predefined list of lockers.

    Args:
        locker_1 (Lockers): A mock locker instance.
        locker_2 (Lockers): Another mock locker instance.

    Returns:
        MagicMock: A mock repository with a predefined return value for get_data().
    """
    repo = MagicMock()
    repo.get_data.return_value = [locker_1, locker_2]
    return repo


@pytest.fixture
def mock_deliver_repo(deliver_1: Delivers, deliver_2: Delivers) -> MagicMock:
    """
    Creates a mock DeliverDataRepository that returns a predefined list of deliveries.

    Args:
        deliver_1 (Delivers): A mock delivery instance.
        deliver_2 (Delivers): Another mock delivery instance.

    Returns:
        MagicMock: A mock repository with a predefined return value for get_data().
    """
    repo = MagicMock()
    repo.get_data.return_value = [deliver_1, deliver_2]
    return repo


@pytest.fixture
def purchase_summary_repo(
        mock_user_repo: UserDataRepository,
        mock_parcel_repo: ParcelDataRepository,
        mock_locker_repo: LockerDataRepository,
        mock_deliver_repo: DeliverDataRepository
) -> PurchaseSummaryRepository:
    """
    Creates an instance of PurchaseSummaryRepository using mock repositories.

    Args:
        mock_user_repo (UserDataRepository): Mocked user repository.
        mock_parcel_repo (ParcelDataRepository): Mocked parcel repository.
        mock_locker_repo (LockerDataRepository): Mocked locker repository.
        mock_deliver_repo (DeliverDataRepository): Mocked deliver repository.

    Returns:
        PurchaseSummaryRepository: An instance of PurchaseSummaryRepository with mock dependencies.
    """
    return PurchaseSummaryRepository[UserDataDict, ParcelsDataDict, LockersDataDict, DeliversDataDict](
        user_repo=mock_user_repo,
        parcel_repo=mock_parcel_repo,
        locker_repo=mock_locker_repo,
        deliver_repo=mock_deliver_repo
    )
