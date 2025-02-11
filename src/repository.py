from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from collections import defaultdict
import logging

from src.file_service import AbstractFileReader, AbstractFileWriter
from src.validator import AbstractValidator
from src.converter import Converter
from src.model import (
    UserDataDict,
    ParcelsDataDict,
    LockersDataDict,
    DeliversDataDict,
    LockerComponentsSize,
    Users,
    City,
    Lockers,
    Parcels,
    Delivers
)

logging.basicConfig(level=logging.INFO)

UsersWithPurchaseDelivers = dict[Users, dict[Delivers, int]]


@dataclass
class AbstractDataRepository[T, U](ABC):
    """
    Abstract repository class for managing data from files. This class handles reading data,
    validating, converting, and caching the processed data.

    Args:
        file_reader (AbstractFileReader[T]): The file reader for reading raw data.
        validator (AbstractValidator[T]): The validator for validating the raw data.
        converter (Converter[T, U]): The converter for converting the raw data into a usable form.
        filename (str | None): The filename to load data from (can be None).
        _data (list[U]): Cached list of processed data (initialized as empty).
    """
    file_reader: AbstractFileReader[T]
    validator: AbstractValidator[T]
    converter: Converter[T, U]
    filename: str | None
    _data: list[U] = field(default_factory=list)

    def __post_init__(self) -> None:
        """
        Initializes the repository and checks that a valid filename is provided.
        If no filename is given, raises an error. Then, it refreshes data from the file.
        """
        if self.filename is None:
            raise ValueError("No filename set")
        self.refresh_data(str(self.filename))

    def get_data(self) -> list[U]:
        """
        Retrieves the cached data. Logs a warning if no data is available.

        Returns:
            list[U]: The processed data list.
        """
        if not self.data:
            logging.warning("No data available in cache")
        return self.data

    def refresh_data(self, filename: str | None = None) -> list[U]:
        """
        Refreshes the cached data by reprocessing the data from the given filename.
        If no filename is provided, uses the default filename.

        Args:
            filename (str | None): Optional custom filename for refreshing data.

        Returns:
            list[U]: The newly processed data.
        """
        if filename is None:
            logging.warning("No filename provided, using default filename")
            filename = self.filename

        logging.info(f"Refreshing data from {self.filename}...")
        self.data = self._process_data(str(self.filename))
        logging.debug(self.data)
        return self.data

    def _process_data(self, filename: str) -> list[U]:
        """
        Reads, validates, and converts the raw data from the given filename.
        Returns a list of successfully processed data.

        Args:
            filename (str): The filename to process.

        Returns:
            list[U]: A list of validated and converted data.
        """
        logging.info(f"Reading data from {filename}...")
        raw_data = self.file_reader.read(filename)
        valid_data = []

        for entry in raw_data:
            if self.validator.validate(entry):
                converted_entry = self.converter.convert(entry)
                valid_data.append(converted_entry)
            else:
                logging.error(f"Invalid entry: {entry}")

        return valid_data


class UserDataRepository(AbstractDataRepository[UserDataDict, Users]):
    """
    Repository class for managing user data. Inherits from AbstractDataRepository and handles
    data specific to users.
    """
    pass


class LockerDataRepository(AbstractDataRepository[LockersDataDict, Lockers]):
    """
    Repository class for managing locker data. Inherits from AbstractDataRepository and handles
    data specific to lockers.
    """
    pass


class ParcelDataRepository(AbstractDataRepository[ParcelsDataDict, Parcels]):
    """
    Repository class for managing parcel data. Inherits from AbstractDataRepository and handles
    data specific to parcels.
    """
    pass


class DeliverDataRepository(AbstractDataRepository[DeliversDataDict, Delivers]):
    """
    Repository class for managing delivery data. Inherits from AbstractDataRepository and handles
    data specific to deliveries.
    """
    pass


@dataclass
class PurchaseSummaryRepository[U, P, L, D]:
    """
    A repository class that aggregates data across users, parcels, lockers, and deliveries
    to generate a purchase summary.

    Args:
        user_repo (AbstractDataRepository[U, Users]): The repository containing user data.
        parcel_repo (AbstractDataRepository[P, Parcels]): The repository containing parcel data.
        locker_repo (AbstractDataRepository[L, Lockers]): The repository containing locker data.
        deliver_repo (AbstractDataRepository[D, Delivers]): The repository containing delivery data.
        _purchase_summary (UsersWithPurchaseDelivers): Cached purchase summary (initialized as empty).
    """
    user_repo: AbstractDataRepository[U, Users]
    parcel_repo: AbstractDataRepository[P, Parcels]
    locker_repo: AbstractDataRepository[L, Lockers]
    deliver_repo: AbstractDataRepository[D, Delivers]
    _purchase_summary: UsersWithPurchaseDelivers = field(default_factory=dict, init=False)

    def purchase_summary(self, force_refresh: bool = False) -> UsersWithPurchaseDelivers:
        """
        Retrieves the purchase summary. If forced or not already cached, refreshes the data.

        Args:
            force_refresh (bool): If True, forces a refresh of the summary.

        Returns:
            UsersWithPurchaseDelivers: The aggregated purchase summary data.
        """
        if force_refresh or not self._purchase_summary:
            logging.info('Building or refreshing purchase summary from repositories ...')
            self._purchase_summary = self._build_purchase_summary()
        return self._purchase_summary

    def _build_purchase_summary(self) -> UsersWithPurchaseDelivers:
        """
        Builds the purchase summary by aggregating data from users, parcels, lockers, and deliveries.

        Returns:
            UsersWithPurchaseDelivers: The aggregated purchase summary.
        """
        purchase_summary: UsersWithPurchaseDelivers = defaultdict(lambda: defaultdict(int))
        users = {user.email: user for user in self.user_repo.get_data()}
        lockers = {locker.locker_id: locker for locker in self.locker_repo.get_data()}
        parcels = {parcel.parcel_id: parcel for parcel in self.parcel_repo.get_data()}
        delivers = self.deliver_repo.get_data()

        for deliver in delivers:
            user = users.get(deliver.sender_email)
            locker = lockers.get(deliver.locker_id)
            parcel = parcels.get(deliver.parcel_id)
            if user and locker and parcel:
                purchase_summary[user][deliver] += 1
            else:
                logging.warning(f'deliver {deliver.sender_email} has invalid user or locker or parcel reference')

        return dict(purchase_summary)
