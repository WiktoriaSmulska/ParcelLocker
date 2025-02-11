from src.model import (
    Delivers,
    Users,
    Parcels,
    Lockers
)
import pytest

@pytest.fixture
def users(user1: Users, user2: Users) -> list[Users]:
    """Fixture that returns a list of user instances."""
    return [user1, user2]

@pytest.fixture
def parcels(parcel1: Parcels, parcel2: Parcels) -> list[Parcels]:
    """Fixture that returns a list of parcel instances."""
    return [parcel1, parcel2]

@pytest.fixture
def lockers(locker1: Lockers, locker2: Lockers) -> list[Lockers]:
    """Fixture that returns a list of locker instances."""
    return [locker1, locker2]

@pytest.fixture
def delivers(deliver1: Delivers, deliver2: Delivers) -> list[Delivers]:
    """Fixture that returns a list of delivery instances."""
    return [deliver1, deliver2]
