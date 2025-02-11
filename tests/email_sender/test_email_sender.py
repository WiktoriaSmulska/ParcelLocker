import os

import pytest
from unittest.mock import patch, MagicMock
from src.email_sender import EmailSender


@pytest.fixture
def email_sender():
    """
    Fixture to create an instance of EmailSender with environment variables.

    :return: EmailSender instance
    """
    return EmailSender(
        smtp_server=str(os.getenv('SMTP_SERVER')),
        port=str(os.getenv('PORT', 587)),
        sender_email=str(os.getenv('SENDER_EMAIL')),
        sender_password=str(os.getenv('SENDER_PASSWORD'))
    )


@patch("src.email_sender.smtplib.SMTP")
def test_send_email_general(mock_smtp, email_sender, capsys):
    """
    Tests the send_email method of EmailSender to verify if an email is sent successfully.

    :param mock_smtp: Mocked SMTP library instance.
    :param email_sender: EmailSender instance from fixture.
    :param capsys: Pytest fixture to capture stdout and stderr.
    """
    mock_smtp_instance = mock_smtp.return_value

    email_sender.send_email(
        recipient_email="wiktoriasmulska0@gmail.com",
        subject="Test Email",
        body="Test Body",
        attachment_path=r'C:\Users\User\Desktop\proj\projects_python\projectt\data\report.txt'
    )

    captured = capsys.readouterr()

    assert "Email sent successfully" in captured.out