from abc import ABC
from src.model import UserDataDict, LockersDataDict, DeliversDataDict, ParcelsDataDict, Lockers, Delivers, Parcels
import json


class AbstractFileReader[T](ABC):
    """
    An abstract base class for reading JSON files and loading them into a list of objects.

    This class provides a generic method for reading data from a file and deserializing it into Python objects.

    Methods:
        read(filename: str) -> list[T]: Reads data from the specified file and returns it as a list of objects.
    """

    def read(self, filename: str) -> list[T]:
        """
        Reads a JSON file and returns its content as a list of objects.

        :param filename: The path to the file to be read.
        :return: A list of objects loaded from the JSON file.
        """
        with open(filename, 'r', encoding='utf8') as file:
            return json.load(file)


class UserJsonFileReader(AbstractFileReader[UserDataDict]):
    """
    A concrete class for reading user data from a JSON file.

    This class inherits from `AbstractFileReader` and specifies that the data being read is of type `UserDataDict`.
    """
    pass


class LockerJsonFileReader(AbstractFileReader[LockersDataDict]):
    """
    A concrete class for reading locker data from a JSON file.

    This class inherits from `AbstractFileReader` and specifies that the data being read is of type `LockersDataDict`.
    """
    pass


class DeliverJsonFileReader(AbstractFileReader[DeliversDataDict]):
    """
    A concrete class for reading delivery data from a JSON file.

    This class inherits from `AbstractFileReader` and specifies that the data being read is of type `DeliversDataDict`.
    """
    pass


class ParcelJsonFileReader(AbstractFileReader[ParcelsDataDict]):
    """
    A concrete class for reading parcel data from a JSON file.

    This class inherits from `AbstractFileReader` and specifies that the data being read is of type `ParcelsDataDict`.
    """
    pass


class AbstractFileWriter[T](ABC):
    """
    An abstract base class for writing objects to a JSON file.

    This class provides a generic method for serializing a list of objects and writing it to a JSON file.

    Methods:
        write(filename: str, data: list[T]) -> None: Writes a list of objects to a JSON file.
    """

    def write(self, filename: str, data: list[T]) -> None:
        """
        Writes a list of objects to a JSON file.

        :param filename: The path to the file where the data will be written.
        :param data: A list of objects to be written to the file.
        """
        with open(filename, 'w', encoding='utf8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


class UserJsonFileWriter(AbstractFileWriter[UserDataDict]):
    """
    A concrete class for writing user data to a JSON file.

    This class inherits from `AbstractFileWriter` and specifies that the data being written is of type `UserDataDict`.
    """
    pass


class LockerJsonFileWriter(AbstractFileWriter[LockersDataDict]):
    """
    A concrete class for writing locker data to a JSON file.

    This class inherits from `AbstractFileWriter` and specifies that the data being written is of type `LockersDataDict`.
    """
    pass


class DeliverJsonFileWriter(AbstractFileWriter[DeliversDataDict]):
    """
    A concrete class for writing delivery data to a JSON file.

    This class inherits from `AbstractFileWriter` and specifies that the data being written is of type `DeliversDataDict`.
    """
    pass


class ParcelJsonFileWriter(AbstractFileWriter[ParcelsDataDict]):
    """
    A concrete class for writing parcel data to a JSON file.

    This class inherits from `AbstractFileWriter` and specifies that the data being written is of type `ParcelsDataDict`.
    """
    pass
