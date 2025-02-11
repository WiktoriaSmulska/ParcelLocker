from enum import Enum
from dataclasses import dataclass
from datetime import date

# Type aliases for dictionary-like structures
UserDataDict = dict[str, str | int | float]
ParcelsDataDict = dict[str, str | int]
LockersDataDict = dict[str, str | int | float | dict[str, int]]
DeliversDataDict = dict[str, str | int | date]


class LockerComponentsSize(Enum):
    """
    Enum representing the available sizes of locker components.

    Values:
        SMALL: Represents a small-sized locker compartment.
        MEDIUM: Represents a medium-sized locker compartment.
        LARGE: Represents a large-sized locker compartment.
    """
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class City(Enum):
    """
    Enum representing various cities.

    Values:
        NEW_YORK: Represents New York City.
        LOS_ANGELES: Represents Los Angeles.
        CHICAGO: Represents Chicago.
        SAN_FRANCISCO: Represents San Francisco.
    """
    NEW_YORK = "New York"
    LOS_ANGELES = "Los Angeles"
    CHICAGO = "Chicago"
    SAN_FRANCISCO = "San Francisco"


@dataclass(frozen=True)
class Users:
    """
    A class representing a user in the system.

    Attributes:
        email (str): The user's email address.
        name (str): The user's first name.
        surname (str): The user's last name.
        city (City): The city where the user is located.
        latitude (float): The user's latitude coordinate.
        longitude (float): The user's longitude coordinate.

    Methods:
        to_dict() -> UserDataDict: Converts the user object to a dictionary representation.
    """
    email: str
    name: str
    surname: str
    city: City
    latitude: float
    longitude: float

    def to_dict(self) -> UserDataDict:
        """
        Converts the user object to a dictionary representation.

        :return: A dictionary containing user data with keys: 'email', 'name', 'surname', 'city', 'latitude', 'longitude'.
        """
        return {
            "email": self.email,
            "name": self.name,
            "surname": self.surname,
            "city": self.city.value,
            "latitude": float(self.latitude),
            "longitude": float(self.longitude)
        }


@dataclass(frozen=True)
class Parcels:
    """
    A class representing a parcel in the system.

    Attributes:
        parcel_id (str): The unique identifier of the parcel.
        height (int): The height of the parcel in centimeters.
        length (int): The length of the parcel in centimeters.
        weight (int): The weight of the parcel in grams.

    Methods:
        to_dict() -> ParcelsDataDict: Converts the parcel object to a dictionary representation.
    """
    parcel_id: str
    height: int
    length: int
    weight: int

    def to_dict(self) -> ParcelsDataDict:
        """
        Converts the parcel object to a dictionary representation.

        :return: A dictionary containing parcel data with keys: 'parcel_id', 'height', 'length', 'weight'.
        """
        return {
            "parcel_id": self.parcel_id,
            "height": self.height,
            "length": self.length,
            "weight": self.weight
        }


@dataclass(frozen=True)
class Lockers:
    """
    A class representing a locker in the system.

    Attributes:
        locker_id (str): The unique identifier of the locker.
        city (City): The city where the locker is located.
        latitude (float): The latitude coordinate of the locker.
        longitude (float): The longitude coordinate of the locker.
        compartments (dict): A dictionary representing the number of available compartments of different sizes.

    Methods:
        to_dict() -> LockersDataDict: Converts the locker object to a dictionary representation.
    """
    locker_id: str
    city: City
    latitude: float
    longitude: float
    compartments: dict[LockerComponentsSize, int]

    def to_dict(self) -> LockersDataDict:
        """
        Converts the locker object to a dictionary representation.

        :return: A dictionary containing locker data with keys: 'locker_id', 'city', 'latitude', 'longitude', 'compartments'.
        """
        return {
            "locker_id": self.locker_id,
            "city": self.city.value,
            "latitude": float(self.latitude),
            "longitude": float(self.longitude),
            "compartments": {
                LockerComponentsSize.SMALL.value: self.compartments.get(LockerComponentsSize.SMALL, 0),
                LockerComponentsSize.MEDIUM.value: self.compartments.get(LockerComponentsSize.MEDIUM, 0),
                LockerComponentsSize.LARGE.value: self.compartments.get(LockerComponentsSize.LARGE, 0)
            }
        }


@dataclass(frozen=True)
class Delivers:
    """
    A class representing a delivery in the system.

    Attributes:
        parcel_id (str): The unique identifier of the parcel being delivered.
        locker_id (str): The unique identifier of the locker where the parcel is being stored.
        sender_email (str): The email address of the sender.
        receiver_email (str): The email address of the receiver.
        sent_date (date): The date the parcel was sent.
        expected_delivery_date (date): The expected delivery date for the parcel.

    Methods:
        to_dict() -> DeliversDataDict: Converts the delivery object to a dictionary representation.
    """
    parcel_id: str
    locker_id: str
    sender_email: str
    receiver_email: str
    sent_date: date
    expected_delivery_date: date

    def to_dict(self) -> DeliversDataDict:
        """
        Converts the delivery object to a dictionary representation.

        :return: A dictionary containing delivery data with keys: 'parcel_id', 'locker_id', 'sender_email', 'receiver_email', 'sent_date', 'expected_delivery_date'.
        """
        return {
            "parcel_id": self.parcel_id,
            "locker_id": self.locker_id,
            "sender_email": self.sender_email,
            "receiver_email": self.receiver_email,
            "sent_date": self.sent_date,
            "expected_delivery_date": self.expected_delivery_date
        }
