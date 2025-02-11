import logging
from dataclasses import dataclass
from src.service import PurchaseSummaryService

logging.basicConfig(level=logging.DEBUG)

@dataclass
class ReportGenerator:
    """
    A class that generates a report based on parcel delivery data.

    Attributes:
        service (PurchaseSummaryService): A service containing data about parcels, lockers, and deliveries.
    """
    service: PurchaseSummaryService

    def generate_report(self, path: str) -> None:
        """
        Generates the entire report and saves it to a specified file path.

        This method calls various internal methods to generate sections of the report
        and writes them to a file.

        Args:
            path (str): The file path where the report will be saved.
        """
        with open(path, "w") as file:
            file.write(self._generate_parcel_sizes_section())
            file.write(self._generate_locker_usage_section())
            file.write(self._generate_popular_sizes_section())
            file.write(self._generate_farthest_users_section())
            file.write(self._generate_longest_delivery_section())

        print(f"Report has been saved to file: {path}")

    def _generate_parcel_sizes_section(self) -> str:
        """
        Generates the section of the report that lists parcel sizes.

        This method iterates over all parcels and retrieves the size of each parcel using
        the `get_parcel_size` method from the service. It then formats and returns the section
        as a string.

        Returns:
            str: A string containing the parcel sizes section of the report.
        """
        section = "=== Parcel Sizes ===\n"
        for parcel_id, parcel in self.service.parcels.items():
            size = self.service.get_parcel_size(parcel)
            section += f"Parcel ID: {parcel_id}, Size: {size}\n"
        section += "\n"
        return section

    def _generate_locker_usage_section(self) -> str:
        """
        Generates the section of the report that details the most frequently used parcel sizes
        per locker.

        This method calls the `most_often_used_size_of_parcel` method from the service to retrieve
        the most used parcel sizes per locker and formats the section accordingly.

        Returns:
            str: A string containing the locker usage section of the report.
        """
        section = "=== Locker_usage_section ===\n"
        most_popular_sizes = self.service.most_often_used_size_of_parcel()
        for locker_id, sizes in most_popular_sizes.items():
            section += f"Locker ID: {locker_id}, Most Frequently Used Sizes: {', '.join(map(str, sizes))}\n"
        section += "\n"
        return section

    def _generate_popular_sizes_section(self) -> str:
        """
        Generates the section of the report that lists the most frequently used parcel sizes.

        This section is similar to the locker usage section but focuses specifically
        on the most popular parcel sizes across all lockers.

        Returns:
            str: A string containing the popular sizes section of the report.
        """
        section = "=== Most Frequently Used Parcel Sizes ===\n"
        most_popular_sizes = self.service.most_often_used_size_of_parcel()
        for locker_id, sizes in most_popular_sizes.items():
            section += f"Locker ID: {locker_id}, Most Frequently Used Sizes: {', '.join(map(str, sizes))}\n"
        section += "\n"
        return section

    def _generate_farthest_users_section(self) -> str:
        """
        Generates the section of the report listing senders and recipients with the farthest deliveries.

        This method calls `person_who_sended_and_picked_up_packages` from the service, which returns
        the farthest senders and recipients. It then formats and adds their details to the report.

        Returns:
            str: A string containing the section about senders and recipients with the farthest deliveries.
        """
        section = "=== Senders and Recipients with Farthest Deliveries ===\n"
        farthest_senders, farthest_receivers = self.service.person_who_sended_and_picked_up_packages(1)
        section += "Farthest Senders:\n"
        for email, details in farthest_senders.items():
            section += f"  {email}, Farthest Locker: {details['farthest_locker']}, Distance: {details['max_distance']} km\n"
        section += "\nFarthest Recipients:\n"
        for email, details in farthest_receivers.items():
            section += f"  {email}, Farthest Locker: {details['farthest_locker']}, Distance: {details['max_distance']} km\n"
        section += "\n"
        return section

    def _generate_longest_delivery_section(self) -> str:
        """
        Generates the section of the report that lists the sender with the longest delivery time.

        This method calls `longest_delivery` from the service to retrieve the sender with the longest
        delivery time and formats it for the report.

        Returns:
            str: A string containing the section about the longest delivery.
        """
        section = "=== Longest Delivery ===\n"
        max_sender, longest_time = self.service.longest_delivery()
        section += f"Sender: {max_sender}, Longest Delivery Time: {longest_time} days\n"
        section += "\n"
        return section
