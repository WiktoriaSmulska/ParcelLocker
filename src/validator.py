from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from src.model import UserDataDict, ParcelsDataDict, LockersDataDict, DeliversDataDict, LockerComponentsSize, Users, \
    City
from decimal import Decimal, InvalidOperation
from enum import Enum
from typing import Type, override
from datetime import date
from email_validator import validate_email, EmailNotValidError
import re
import logging

logging.basicConfig(level=logging.INFO)


@dataclass
class AbstractValidator[T](ABC):
    """
    Abstract base class for validating data of type T.
    Subclasses should define the validation logic specific to each data type.

    Args:
        required_keys (list[str]): List of required keys that the data must contain.
    """
    required_keys: list[str] = field(default_factory=list)

    def validate(self, data: T) -> bool:
        """
        Validates that the data contains the required keys and passes any additional
        specific validation logic.

        Args:
            data (T): The data to be validated.

        Returns:
            bool: True if the data is valid, otherwise False.
        """
        return len(self.required_keys) == 0 or self.has_required_keys(data, self.required_keys)

    def has_required_keys(self, data: T, keys: list[str]) -> bool:
        """
        Checks if the data contains all required keys.

        Args:
            data (T): The data to be validated.
            keys (list[str]): The list of required keys to check for.

        Returns:
            bool: True if all required keys are present, otherwise False.
        """
        missing_keys = []
        for key in keys:
            if isinstance(data, dict):
                if key not in data:
                    missing_keys.append(key)
            elif not hasattr(data, key):
                missing_keys.append(key)

        if missing_keys:
            logging.error(f"Missing required keys: {missing_keys}")
            return False
        return True

    @staticmethod
    def is_positive(data: int | str | None) -> bool:
        """
        Checks if the given data is a positive number.

        Args:
            data (int | str | None): The data to check.

        Returns:
            bool: True if the data is a positive number, otherwise False.
        """
        if isinstance(data, int):
            return data > 0
        if isinstance(data, str):
            try:
                decimal_value = Decimal(data)
                return decimal_value > 0
            except InvalidOperation as e:
                logging.error(str(e))
        return False

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Validates an email address.

        Args:
            email (str): The email address to validate.

        Returns:
            bool: True if the email is valid, otherwise False.
        """
        try:
            validate_email(email, check_deliverability=True)
            return True
        except EmailNotValidError as e:
            logging.error(str(e))
            return False

    @staticmethod
    def validate_string_with_regex(value: str, pattern: str) -> bool:
        """
        Validates a string using a regular expression pattern.

        Args:
            value (str): The string to validate.
            pattern (str): The regular expression pattern.

        Returns:
            bool: True if the string matches the pattern, otherwise False.
        """
        return re.fullmatch(pattern, value) is not None

    @staticmethod
    def is_valid_value_of(value: str | float | dict[str, int] | int, enum_class: Type[Enum]) -> bool:
        """
        Checks if a value is a valid member of an enum class.

        Args:
            value (str | float | dict[str, int] | int): The value to check.
            enum_class (Type[Enum]): The enum class to check the value against.

        Returns:
            bool: True if the value is valid in the enum, otherwise False.
        """
        if isinstance(value, str):
            return value in [item.value for item in enum_class]
        return False

    @staticmethod
    def are_compartments_non_negative(compartments: dict[LockerComponentsSize, int]) -> bool:
        """
        Checks if all compartment values in the dictionary are non-negative integers.

        Args:
            compartments (dict[LockerComponentsSize, int]): The compartments to check.

        Returns:
            bool: True if all compartment values are non-negative, otherwise False.
        """
        return all(isinstance(value, int) and int(value) > 0 for value in compartments.values())

    @staticmethod
    def are_sizes_bigger_than_zero(parcel: ParcelsDataDict) -> bool:
        """
        Validates that all parcel dimensions (height, length, weight) are greater than zero.

        Args:
            parcel (ParcelsDataDict): The parcel data to check.

        Returns:
            bool: True if all dimensions are greater than zero, otherwise False.
        """
        return all(
            isinstance(parcel.get(dim), int)
            and int(parcel.get(dim, 0)) > 0
            for dim in ['height', 'length', 'weight']
        )

    @staticmethod
    def check_to_who_packed_is_send(deliver: DeliversDataDict) -> bool:
        """
        Validates that the sender and receiver emails are different.

        Args:
            deliver (DeliversDataDict): The delivery data to check.

        Returns:
            bool: True if the sender and receiver emails are different, otherwise False.
        """
        sender_email = deliver.get("sender_email")
        receiver_email = deliver.get("receiver_email")

        if sender_email is None or receiver_email is None:
            return False

        return sender_email != receiver_email

    @staticmethod
    def check_if_dates_of_delivery_are_different(deliver: DeliversDataDict) -> bool:
        """
        Validates that the delivery's send date is not later than the expected delivery date.

        Args:
            deliver (DeliversDataDict): The delivery data to check.

        Returns:
            bool: True if the send date is earlier than or equal to the expected delivery date, otherwise False.
        """
        send_date = deliver.get("send_date")
        expected_date = deliver.get("expected_delivery_date")

        if isinstance(send_date, date) and isinstance(expected_date, date):
            return send_date <= expected_date

        return False


@dataclass
class UserDataDictValidator(AbstractValidator[UserDataDict]):
    """
    Concrete validator for user data dictionaries.

    Inherits from AbstractValidator to validate user data, such as email, name, and coordinates.
    """

    def __post_init__(self):
        if len(self.required_keys) == 0:
            self.required_keys = ["email", "name", "surname", "city", "latitude", "longitude"]

    @override
    def validate(self, data: UserDataDict) -> bool:
        """
        Validates user data.

        Args:
            data (UserDataDict): The user data to validate.

        Returns:
            bool: True if the user data is valid, otherwise False.
        """
        email = data.get("email")
        if isinstance(email, str):
            return super().validate(data) and AbstractValidator.is_valid_email(email)
        return False


@dataclass
class ParcelDataDictValidator(AbstractValidator[ParcelsDataDict]):
    """
    Concrete validator for parcel data dictionaries.

    Inherits from AbstractValidator to validate parcel data such as size and weight.
    """

    def __post_init__(self):
        if len(self.required_keys) == 0:
            self.required_keys = ["parcel_id", "height", "length", "weight"]

    @override
    def validate(self, data: ParcelsDataDict) -> bool:
        """
        Validates parcel data.

        Args:
            data (ParcelsDataDict): The parcel data to validate.

        Returns:
            bool: True if the parcel data is valid, otherwise False.
        """
        return (
                super().validate(data)
                and AbstractValidator.is_positive(data.get("weight"))
                and AbstractValidator.is_positive(data.get("length"))
                and AbstractValidator.is_positive(data.get("height"))
        )


@dataclass
class LockerDataDictValidator(AbstractValidator[LockersDataDict]):
    """
    Concrete validator for locker data dictionaries.

    Inherits from AbstractValidator to validate locker data, including city and compartments.
    """

    def __post_init__(self):
        if len(self.required_keys) == 0:
            self.required_keys = ["locker_id", "city", "latitude", "longitude", "compartments"]

    @override
    def validate(self, data: LockersDataDict) -> bool:
        """
        Validates locker data.

        Args:
            data (LockersDataDict): The locker data to validate.

        Returns:
            bool: True if the locker data is valid, otherwise False.
        """
        return super().validate(data) and AbstractValidator.is_valid_value_of(data["city"], City)


@dataclass
class DeliverDataDictValidator(AbstractValidator[DeliversDataDict]):
    """
    Concrete validator for delivery data dictionaries.

    Inherits from AbstractValidator to validate delivery data, such as sender, receiver, and dates.
    """

    def __post_init__(self):
        if len(self.required_keys) == 0:
            self.required_keys = ["parcel_id", "locker_id", "sender_email", "receiver_email", "sent_date",
                                  "expected_delivery_date"]

    @override
    def validate(self, data: DeliversDataDict) -> bool:
        """
        Validates delivery data.

        Args:
            data (DeliversDataDict): The delivery data to validate.

        Returns:
            bool: True if the delivery data is valid, otherwise False.
        """
        return super().validate(data) and AbstractValidator.check_to_who_packed_is_send(data)
