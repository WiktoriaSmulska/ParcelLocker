from dataclasses import dataclass
from src.repository import AbstractDataRepository


@dataclass
class SpeechRecognizerService:
    """
    A service class responsible for handling package-related operations, such as finding lockers
    for a given package and reading a report from a file. It interacts with a data repository to
    retrieve package information.
    """

    deliver_repo: AbstractDataRepository

    def __post_init__(self):
        """
        Initializes the service by loading package data from the repository and storing it in a dictionary
        for quick lookups by parcel ID. This is called automatically after the class is instantiated.
        """
        self.delivers = {deliver.parcel_id: deliver for deliver in self.deliver_repo.get_data()}

    def find_locker(self, number: str) -> str:
        """
        Finds the locker where a specific package is located based on the given parcel number.

        Args:
            number (str): The parcel number for which the locker needs to be found.

        Returns:
            str: A message indicating whether the package exists and the locker number if available.
        """
        correct_num = number.strip().upper()  # Ensures the parcel number is clean and in uppercase
        if correct_num not in self.delivers.keys():
            return f"Your package does not exist"

        locker_num = self.delivers[correct_num].locker_id  # Get locker id from the deliver object
        return f"Your package {correct_num} is in locker {locker_num}"

    def read_report(self):
        """
        Reads and returns the content of a report file located on the desktop.

        Returns:
            str: The content of the report read from the file.
        """
        with open(r"C:\Users\User\Desktop\proj\projects_python\projectt\data\report.txt", "r") as file:
            data = file.read()
        return data
