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
    Delivers
)
from typing import cast
import pytest

def test_initial_state_empty_cache(purchase_summary_repo: PurchaseSummaryRepository) -> None:
    """
    Test that the initial state of the purchase summary repository cache is empty.

    Args:
        purchase_summary_repo (PurchaseSummaryRepository): The repository instance being tested.

    Assertions:
        - The internal `_purchase_summary` cache is initially empty.
    """
    assert purchase_summary_repo._purchase_summary == {}

def test_purchase_summary_build_cache(
    purchase_summary_repo: PurchaseSummaryRepository,
    user_1: Users,
    user_2: Users,
    parcel_1: Parcels,
    parcel_2: Parcels,
    locker_1: Lockers,
    locker_2: Lockers,
    deliver_1: Delivers,
    deliver_2: Delivers
) -> None:
    """
    Test that the purchase summary repository correctly builds and caches the purchase summary.

    Args:
        purchase_summary_repo (PurchaseSummaryRepository): The repository instance.
        user_1 (Users): First user instance.
        user_2 (Users): Second user instance.
        parcel_1 (Parcels): First parcel instance.
        parcel_2 (Parcels): Second parcel instance.
        locker_1 (Lockers): First locker instance.
        locker_2 (Lockers): Second locker instance.
        deliver_1 (Delivers): First delivery instance.
        deliver_2 (Delivers): Second delivery instance.

    Assertions:
        - The summary contains two users.
        - Each user has exactly one delivery associated.
    """
    summary = purchase_summary_repo.purchase_summary()

    assert len(summary) == 2

    us_1 = summary.get(user_1)
    assert us_1 is not None
    assert us_1[deliver_1] == 1

    us_2 = summary.get(user_2)
    assert us_2 is not None
    assert us_2[deliver_2] == 1

def test_purchase_summary_cache_reuse(purchase_summary_repo: PurchaseSummaryRepository) -> None:
    """
    Test that the purchase summary repository correctly reuses the cache.

    Args:
        purchase_summary_repo (PurchaseSummaryRepository): The repository instance.

    Assertions:
        - The summary is cached and contains existing data.
        - Adding a new user does not trigger a cache refresh.
    """
    summary = purchase_summary_repo.purchase_summary()
    assert len(summary) > 0

    user_repo_mock = cast(MagicMock, purchase_summary_repo.user_repo.get_data)
    user_repo_mock.return_value.append(
        Users(
            email="bob.jones@gmail.com",
            name="Bob",
            surname="Jones",
            city=City.NEW_YORK,
            latitude=37.774929,
            longitude=-122.419418
        )
    )

    summary = purchase_summary_repo.purchase_summary()
    assert len(summary) == 2

def test_purchase_summary_force_refresh(
    purchase_summary_repo: PurchaseSummaryRepository,
    user_1: Users,
    user_2: Users,
    deliver_1: Delivers,
) -> None:
    """
    Test that forcing a refresh correctly updates the purchase summary.

    Args:
        purchase_summary_repo (PurchaseSummaryRepository): The repository instance.
        user_1 (Users): First user instance.
        user_2 (Users): Second user instance.
        deliver_1 (Delivers): First delivery instance.

    Assertions:
        - The cache is rebuilt when force_refresh=True.
        - The new delivery entry is correctly added to the summary.
    """
    _ = purchase_summary_repo.purchase_summary()

    new_deliver = Delivers(
        parcel_id="P67890",
        locker_id="L002",
        sender_email="bob.jones@gmail.com",
        receiver_email="mark.taylor@example.com",
        sent_date=date(2023, 12, 4),
        expected_delivery_date=date(2023, 12, 8),
    )
    deliver_repo_mock = cast(MagicMock, purchase_summary_repo.deliver_repo.get_data)
    deliver_repo_mock.return_value.append(new_deliver)

    summary = purchase_summary_repo.purchase_summary(force_refresh=True)
    assert len(summary) == 2

    user_1_summary = summary.get(user_1)
    assert user_1_summary is not None
    assert user_1_summary[deliver_1] == 1
    assert user_1_summary[new_deliver] == 1

    user_2_summary = summary.get(user_2)
    assert user_2_summary is not None
    assert len(user_2_summary) == 1

def test_invalid_entry_logs_warning(
    purchase_summary_repo: PurchaseSummaryRepository,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """
    Test that an invalid delivery entry logs a warning message.

    Args:
        purchase_summary_repo (PurchaseSummaryRepository): The repository instance.
        caplog (pytest.LogCaptureFixture): Fixture to capture log output.

    Assertions:
        - A warning message is logged when an invalid entry is encountered.
    """
    invalid_deliver = Delivers(
        parcel_id="P99999",
        locker_id="L999",
        sender_email="nonexistent.sender@example.com",
        receiver_email="nonexistent.receiver@example.com",
        sent_date=date(2023, 12, 4),
        expected_delivery_date=date(2023, 12, 8),
    )

    deliver_repo_mock = cast(MagicMock, purchase_summary_repo.deliver_repo.get_data)
    deliver_repo_mock.return_value.append(invalid_deliver)

    with caplog.at_level("WARNING"):
        _ = purchase_summary_repo.purchase_summary(force_refresh=True)
        assert any(
            "invalid user or locker or parcel reference" in record.message
            for record in caplog.records
        )
