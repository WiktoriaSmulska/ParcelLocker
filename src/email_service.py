from dataclasses import dataclass
from src.email_sender import EmailSender
from src.model import Parcels, Users, LockerComponentsSize
from src.report_generate import ReportGenerator
from src.service import PurchaseSummaryService
from dataclasses import dataclass
from geopy.distance import geodesic # type: ignore[import]
import logging
import os
logging.basicConfig(level=logging.DEBUG)

@dataclass
class EmailService:
    """
    A service for sending emails related to parcels, lockers, and user notifications.

    Attributes:
        service (PurchaseSummaryService): A service that contains users, lockers, and delivery data.
    """
    service: PurchaseSummaryService


    def __post_init__(self)->None:
        """
        Initializes the EmailService instance by extracting necessary information
        from the PurchaseSummaryService instance, including users, lockers, and deliveries.
        Additionally, it retrieves SMTP configuration from environment variables.
        """

        self.users = self.service.users
        self.lockers = self.service.lockers
        self.delivers = {deliver.locker_id : deliver for deliver in self.service.deliver_repo.get_data()}
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.port = os.getenv('PORT')
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')


    def generate_report(self):
        """
        Generates a report by calling the ReportGenerator and saves it to a file.

        The report contains a summary of parcel deliveries.
        """
        report_gen = ReportGenerator(self.service)
        report_gen.generate_report("data/report.txt")

    def generate_and_send_email_to_all_users(self, subject:str, body:str, attachment_path:str):
        """
        Generates a report and sends it via email to all users.

        This method first generates a report and then sends an email to all registered users
        with the specified subject, body, and attachment.

        Args:
            subject (str): The subject of the email.
            body (str): The body of the email.
            attachment_path (str): The path to the file that should be attached to the email.
        """
        self.generate_report()
        if self.smtp_server is not None and self.port is not None and self.sender_email is not None and self.sender_password is not None:
            for recipient_mail in self.users:
                email_sender = EmailSender(self.smtp_server, self.port, self.sender_email, self.sender_password)
                email_sender.send_email(recipient_mail, subject, body, attachment_path)

    def send_email(self, recipient_mail:str, subject:str, body:str, attachment_path:str | None = None):
        """
        Sends an email to a specific recipient with the specified subject and body,
        optionally including an attachment.

        Args:
            recipient_mail (str): The email address of the recipient.
            subject (str): The subject of the email.
            body (str): The body of the email.
            attachment_path (str | None): The path to the file to attach (optional).
        """
        if self.smtp_server is not None and self.port is not None and self.sender_email is not None and self.sender_password is not None:
            email_sender = EmailSender(self.smtp_server, self.port, self.sender_email, self.sender_password)
            email_sender.send_email(recipient_mail, subject, body, attachment_path)

    def send_email_about_free_locker(self, email: str, parcel: Parcels):
        """
        Sends an email to the user about the availability of a locker for their parcel.

        This method finds an available locker and sends an email to the user with the locker details
        such as locker ID and the status of compartments (small, medium, large).

        Args:
            email (str): The user's email address.
            parcel (Parcels): The parcel object containing parcel details.
        """
        locker_id, s, m, l= self.find_parcel_locker(email, parcel)
        subject= "information about locker"
        body = f"locker {locker_id} is ,status of the compartments small: {s}, medium: {m}, large: {l}, you can send your packed there"
        if locker_id is not None:
            self.send_email(email, subject, body, None)
            self.send_email_to_receiver(locker_id, True)

    def send_email_to_receiver(self, locker: str, package_in_locker: bool):
        """
        Sends an email to the receiver about the status of the package in the locker.

        This method sends a notification email to the receiver informing them that their package
        has been sent to the locker and provides the expected delivery date.

        Args:
            locker (str): The locker ID where the package is placed.
            package_in_locker (bool): Whether the package is in the locker or not.
        """
        if not package_in_locker:
            logging.info("package is not in locker yet")

        deliver = self.delivers.get(locker)
        if deliver and package_in_locker:
            email = deliver.receiver_email

            subject = "package"
            body = f"package is send to you, you will be able to pick it up in {deliver.expected_delivery_date}"
            self.send_email(email, subject, body, None)


    def find_parcel_locker(self, email: str, parcel: Parcels):
        """
        Finds the closest available locker for a user based on their location and parcel size.

        This method searches for the closest locker that has available compartments for the parcel
        and is within a reasonable distance from the user's location.

        Args:
            email (str): The user's email address.
            parcel (Parcels): The parcel object containing parcel details.

        Returns:
            tuple: A tuple containing the closest locker ID and available compartment sizes (small, medium, large).
            If no locker is found, returns None for all values.
        """
        if email not in self.users:
            logging.info("email is incorrect")
        user = self.users.get(email)

        if not user:
            logging.error("Email is incorrect or not found.")
            return None, None, None, None

        size = self.service.get_parcel_size(parcel)

        user_location = (user.latitude, user.longitude)

        min_distace = float('inf')
        closest_locker_id = None
        available_compartments = {}

        def has_available_compartment(locker, size):
            """
            Checks if a locker has available compartments for the given size.
            """
            return size in locker.compartments and locker.compartments[size] > 0


        for locker_id, locker in self.lockers.items():
            locker_location = (locker.latitude, locker.longitude)
            distance = geodesic(user_location, locker_location).kilometers


            if distance < min_distace and has_available_compartment(locker, size) and locker_id in self.delivers:
                min_distace = distance
                closest_locker_id = locker_id
                available_compartments = locker.compartments

            elif has_available_compartment(locker, size) == False:
                logging.error("No locker found")


        if closest_locker_id is None:
            logging.error(f"No locker found within {min_distace} km radius for the specified parcel size.")
            return None, None,None, None


        return (
            closest_locker_id,
            available_compartments.get(LockerComponentsSize.SMALL),
            available_compartments.get(LockerComponentsSize.MEDIUM),
            available_compartments.get(LockerComponentsSize.LARGE)
        )


