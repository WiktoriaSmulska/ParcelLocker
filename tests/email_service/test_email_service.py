from unittest.mock import patch, MagicMock
from src.email_service import EmailService
from src.model import Parcels
from src.service import PurchaseSummaryService
import pytest
import logging

def test_generate_report(email_service: EmailService, purchase_summary_service: PurchaseSummaryService):
    """
    Tests report generation by ensuring the ReportGenerator is called with the correct parameters.
    """
    with patch("src.email_service.ReportGenerator") as MockReportGenerator:
        mock_report_gen_instance = MagicMock()
        MockReportGenerator.return_value = mock_report_gen_instance

        email_service.generate_report()

        MockReportGenerator.assert_called_once_with(purchase_summary_service)
        mock_report_gen_instance.generate_report.assert_called_once_with("data/report.txt")

def test_generate_and_send_email_to_all_users(email_service: EmailService, purchase_summary_service: PurchaseSummaryService):
    """
    Tests generating and sending emails to all users.
    Ensures that report generation and email sending are correctly invoked.
    """
    with patch("src.email_service.ReportGenerator") as MockReportGenerator, \
         patch("src.email_service.EmailSender") as MockEmailSender:

        mock_report_gen_instance = MagicMock()
        MockReportGenerator.return_value = mock_report_gen_instance

        mock_sender_email_instance = MagicMock()
        MockEmailSender.return_value = mock_sender_email_instance

        with patch.dict("os.environ", {
            "SMTP_SERVER": "smtp.example.com",
            "PORT": "587",
            "SENDER_EMAIL": "sender@example.com",
            "SENDER_PASSWORD": "password123"
        }):
            email_service.generate_and_send_email_to_all_users(
                subject="Test Subject",
                body="This is a test email.",
                attachment_path="data/report.txt"
            )

            mock_report_gen_instance.generate_report.assert_called_once_with("data/report.txt")
            assert MockEmailSender.call_count == len(email_service.users)

            for user_email in email_service.users:
                mock_sender_email_instance.send_email.assert_any_call(
                    user_email,
                    "Test Subject",
                    "This is a test email.",
                    "data/report.txt"
                )

def test_send_email(email_service: EmailService) -> None:
    """
    Tests the send_email method of EmailService by mocking the EmailSender.
    """
    with patch("src.email_service.EmailSender") as MockEmailSender:
        email_sender_instance = MagicMock()
        MockEmailSender.return_value = email_sender_instance

        recipient_mail = "test@example.com"
        subject = "Test Subject"
        body = "This is a test email."
        attachment_path = "data/report.txt"

        email_service.send_email(
            recipient_mail=recipient_mail,
            subject=subject,
            body=body,
            attachment_path=attachment_path
        )

        MockEmailSender.assert_called_once_with(
            email_service.smtp_server,
            email_service.port,
            email_service.sender_email,
            email_service.sender_password
        )

        email_sender_instance.send_email.assert_called_once_with(
            recipient_mail,
            subject,
            body,
            attachment_path
        )

@pytest.mark.parametrize(
    "locker, package_in_locker, expected_log",
    [
        ("L001", False, "package is not in locker yet"),
        ("L002", True, None)
    ],
)
def test_send_email_to_receiver(email_service: EmailService, locker, package_in_locker, expected_log, caplog):
    """
    Tests sending an email to the receiver based on package presence in the locker.
    """
    with patch.object(email_service, "send_email", new=MagicMock()) as mock_send_email:
        with caplog.at_level(logging.INFO):
            email_service.send_email_to_receiver(locker, package_in_locker)

        if expected_log:
            assert expected_log in caplog.text
        else:
            assert "package is not in locker yet" not in caplog.text

        if locker in email_service.delivers and package_in_locker:
            mock_send_email.assert_called_once_with(
                "jane.smith@gmail.com",
                "package",
                "package is send to you, you will be able to pick it up in 2023-12-08",
                None,
            )
        else:
            mock_send_email.assert_not_called()

def test_send_email_about_free_locker(email_service: EmailService, parcel_11: Parcels) -> None:
    """
    Tests sending an email notifying a user about an available locker.
    """
    with patch.object(email_service, "send_email", new=MagicMock()) as mock_send_email, \
            patch.object(email_service, "send_email_to_receiver", new=MagicMock()) as mock_send_email_to_receiver, \
            patch.object(email_service, "find_parcel_locker", new=MagicMock(return_value=("L001", 20, 15, 5))):
        locker, s, m, l = email_service.find_parcel_locker("alice.smith@gmail.com", parcel_11)
        email_service.send_email_about_free_locker("alice.smith@gmail.com", parcel_11)

        mock_send_email.assert_called_once_with(
            "alice.smith@gmail.com",
            "information about locker",
            f"locker {locker} is ,status of the compartments small: {s}, medium: {m}, large: {l}, you can send your packed there",
            None,
        )

        mock_send_email_to_receiver.assert_called_once_with(locker, True)

def test_find_parcel_locker(email_service: EmailService, parcel_11: Parcels, caplog) -> None:
    """
    Tests finding the closest parcel locker and logging appropriate messages.
    """
    closest_locker, small, medium, large = email_service.find_parcel_locker("alice.smith@gmail.com", parcel_11)

    assert closest_locker == "L001"
    assert small == 20
    assert medium == 15
    assert large == 5

    with caplog.at_level(logging.INFO):
        closest_locker, small, medium, large = email_service.find_parcel_locker("alica.smith@gmail.com", parcel_11)

    assert closest_locker is None
    assert small is None
    assert medium is None
    assert large is None
    assert "email is incorrect" in caplog.text
