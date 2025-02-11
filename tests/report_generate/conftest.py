from datetime import date
from unittest.mock import MagicMock
import pytest
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
    Delivers
)
from src.service import PurchaseSummaryService

@pytest.fixture
def user_11() -> Users:
    """Creates a test user located in New York."""
    return Users(
        email="john.doe@gmail.com",
        name="John",
        surname="Doe",
        city=City.NEW_YORK,
        latitude=40.712776,
        longitude=-74.005974
    )

@pytest.fixture
def user_22() -> Users:
    """Creates a test user located in Los Angeles."""
    return Users(
        email="jane.smith@gmail.com",
        name="Jane",
        surname="Smith",
        city=City.LOS_ANGELES,
        latitude=34.052235,
        longitude=-118.243683
    )

@pytest.fixture
def user_33() -> Users:
    """Creates a test user located in Chicago."""
    return Users(
        email="alice.smith@gmail.com",
        name="Alice",
        surname="Smith",
        city=City.CHICAGO,
        latitude=41.878113,
        longitude=-87.629799
    )

@pytest.fixture
def user_44() -> Users:
    """Creates a test user located in San Francisco."""
    return Users(
        email="bob.jones@gmail.com",
        name="Bob",
        surname="Jones",
        city=City.SAN_FRANCISCO,
        latitude=37.774929,
        longitude=-122.419418
    )

@pytest.fixture
def parcel_11():
    """Creates a test parcel with specific dimensions."""
    return Parcels(parcel_id="P12345", height=30, length=50, weight=5)

@pytest.fixture
def parcel_22():
    """Creates another test parcel with different dimensions."""
    return Parcels(parcel_id="P67890", height=20, length=40, weight=4)

@pytest.fixture
def locker_11() -> Lockers:
    """Creates a test locker in New York with available compartments."""
    return Lockers(
        locker_id="L001",
        city=City.NEW_YORK,
        latitude=40.730610,
        longitude=-73.935242,
        compartments={
            LockerComponentsSize.SMALL: 20,
            LockerComponentsSize.MEDIUM: 15,
            LockerComponentsSize.LARGE: 5,
        }
    )

@pytest.fixture
def locker_22() -> Lockers:
    """Creates a test locker in Los Angeles with available compartments."""
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
def deliver_11() -> Delivers:
    """Creates a test delivery record from Alice to John."""
    return Delivers(
        parcel_id="P12345",
        locker_id="L001",
        sender_email="alice.smith@gmail.com",
        receiver_email="john.doe@gmail.com",
        sent_date=date(2023, 12, 1),
        expected_delivery_date=date(2023, 12, 5)
    )

@pytest.fixture
def deliver_22() -> Delivers:
    """Creates another test delivery record from Bob to Jane."""
    return Delivers(
        parcel_id="P67890",
        locker_id="L002",
        sender_email="bob.jones@gmail.com",
        receiver_email="jane.smith@gmail.com",
        sent_date=date(2023, 12, 2),
        expected_delivery_date=date(2023, 12, 8)
    )

@pytest.fixture
def mock_user_repo(user_11, user_22, user_33, user_44) -> MagicMock:
    """Creates a mock user repository returning predefined users."""
    repo = MagicMock()
    repo.get_data.return_value = [user_11, user_22, user_33, user_44]
    return repo

@pytest.fixture
def mock_parcel_repo(parcel_11, parcel_22) -> MagicMock:
    """Creates a mock parcel repository returning predefined parcels."""
    repo = MagicMock()
    repo.get_data.return_value = [parcel_11, parcel_22]
    return repo

@pytest.fixture
def mock_locker_repo(locker_11, locker_22) -> MagicMock:
    """Creates a mock locker repository returning predefined lockers."""
    repo = MagicMock()
    repo.get_data.return_value = [locker_11, locker_22]
    return repo

@pytest.fixture
def mock_deliver_repo(deliver_11, deliver_22) -> MagicMock:
    """Creates a mock delivery repository returning predefined deliveries."""
    repo = MagicMock()
    repo.get_data.return_value = [deliver_11, deliver_22]
    return repo

@pytest.fixture
def purchase_summary_service(
        mock_user_repo,
        mock_parcel_repo,
        mock_locker_repo,
        mock_deliver_repo,
        user_11,
        user_22,
        user_33,
        user_44,
        parcel_11,
        parcel_22,
        locker_11,
        locker_22,
        deliver_11,
        deliver_22
) -> PurchaseSummaryService:
    """Creates an instance of PurchaseSummaryService using mock repositories and predefined test data."""
    return PurchaseSummaryService(
        user_repo=mock_user_repo,
        parcel_repo=mock_parcel_repo,
        locker_repo=mock_locker_repo,
        deliver_repo=mock_deliver_repo,
        lockers={locker_11.locker_id: locker_11, locker_22.locker_id: locker_22},
        parcels={parcel_11.parcel_id: parcel_11, parcel_22.parcel_id: parcel_22},
        delivers=[deliver_11, deliver_22],
        users={user_11.email: user_11, user_22.email: user_22, user_33.email: user_33, user_44.email: user_44},
        locker_usage={locker.locker_id: {'small': 0, 'medium': 0, 'large': 0} for locker in [locker_11, locker_22]}
    )
