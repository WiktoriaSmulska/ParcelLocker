from abc import ABC, abstractmethod
from typing import override
from datetime import date, datetime
from src.model import (
    Users,
    Lockers,
    Parcels,
    Delivers,
    City,
    LockerComponentsSize,
    UserDataDict,
    ParcelsDataDict,
    LockersDataDict,
    DeliversDataDict,
)
import logging

logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.ERROR)


class Converter[T, U](ABC):

    @abstractmethod
    def convert(self, data: T) -> U:
        """
        Abstract method to be implemented by subclasses to convert data of type T into type U.
        """
        pass


class UserConverter(Converter[UserDataDict, Users]):
    @override
    def convert(self, data: UserDataDict) -> Users:
        """
        Converts a dictionary representing user data into a Users object.

        :param data: Dictionary containing user data.
        :return: Users object populated with the given data.
        """
        return Users(
            email=str(data['email']),
            name=str(data['name']),
            surname=str(data['surname']),
            city=City(data['city']),
            latitude=float(data['latitude']),
            longitude=float(data['longitude'])
        )


class ParcelConverter(Converter[ParcelsDataDict, Parcels]):
    @override
    def convert(self, data: ParcelsDataDict) -> Parcels:
        """
        Converts a dictionary representing parcel data into a Parcels object.

        :param data: Dictionary containing parcel data.
        :return: Parcels object populated with the given data.
        """
        return Parcels(
            parcel_id=str(data['parcel_id']),
            height=int(data['height']),
            length=int(data['length']),
            weight=int(data['weight'])
        )


class LockerConverter(Converter[LockersDataDict, Lockers]):
    @override
    def convert(self, data: LockersDataDict) -> Lockers:
        """
        Converts a dictionary representing locker data into a Lockers object,
        ensuring proper handling of missing or incorrect values.

        :param data: Dictionary containing locker data.
        :return: Lockers object populated with the given data.
        """
        compartments = data.get("compartments", {})
        if not isinstance(compartments, dict):
            logging.error("'compartments' is not a dictionary. Using default empty dictionary.")
            compartments = {}

        def safe_float(value, field_name):
            """
            Safely converts a value to float, logging an error if conversion fails.

            :param value: Value to be converted.
            :param field_name: Name of the field being converted.
            :return: Converted float value, or 0.0 if conversion fails.
            """
            try:
                return float(value)
            except (TypeError, ValueError):
                logging.error(f"Invalid type for {field_name}: {value}. Using 0.0 as fallback.")
                return 0.0

        latitude = safe_float(data.get("latitude"), "latitude")
        longitude = safe_float(data.get("longitude"), "longitude")

        return Lockers(
            locker_id=str(data["locker_id"]),
            city=City(data["city"]),
            latitude=latitude,
            longitude=longitude,
            compartments={
                LockerComponentsSize.SMALL: compartments.get("small", 0),
                LockerComponentsSize.MEDIUM: compartments.get("medium", 0),
                LockerComponentsSize.LARGE: compartments.get("large", 0),
            }
        )


class DeliversConverter(Converter[DeliversDataDict, Delivers]):
    @override
    def convert(self, data: DeliversDataDict) -> Delivers:
        """
        Converts a dictionary representing delivery data into a Delivers object,
        handling different date formats safely.

        :param data: Dictionary containing delivery data.
        :return: Delivers object populated with the given data.
        """

        def parse_date(date_value):
            """
            Converts different date formats into a date object.

            :param date_value: Date value which can be a date object, timestamp, or string.
            :return: Parsed date object.
            :raises TypeError: If the date format is unsupported.
            """
            if isinstance(date_value, date):
                return date_value
            if isinstance(date_value, int):
                return datetime.utcfromtimestamp(date_value).date()
            if isinstance(date_value, str):
                return datetime.strptime(date_value, "%Y-%m-%d").date()
            raise TypeError(f"Unsupported type for date parsing: {type(date_value)}")

        logging.debug(data)
        send_date = parse_date(data["sent_date"])
        expected_delivery_date = parse_date(data["expected_delivery_date"])

        return Delivers(
            parcel_id=str(data["parcel_id"]),
            locker_id=str(data["locker_id"]),
            sender_email=str(data["sender_email"]),
            receiver_email=str(data["receiver_email"]),
            sent_date=send_date,
            expected_delivery_date=expected_delivery_date
        )
