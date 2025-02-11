from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import ssl
import os


class EmailSender:
    def __init__(
            self,
            smtp_server: str,
            port: str,
            sender_email: str,
            sender_password: str
    ) -> None:
        """
        Initialize the EmailSender class with necessary credentials and settings.

        :param smtp_server: SMTP server address (e.g., 'smtp.gmail.com')
        :param port: Port number for the SMTP server (e.g., '587')
        :param sender_email: The email address of the sender
        :param sender_password: The password for the sender's email account
        """
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(
            self,
            recipient_email: str,
            subject: str,
            body: str,
            attachment_path: str | None = None
    ):
        """
        Sends an email to the specified recipient with the given subject and body.
        Optionally, an attachment can be added.

        :param recipient_email: The email address of the recipient
        :param subject: The subject of the email
        :param body: The body text of the email
        :param attachment_path: Optional path to a file to be attached to the email
        """


        message = MIMEMultipart("alternative")
        message["From"] = self.sender_email
        message["To"] = recipient_email
        message["Subject"] = subject

        text_part = MIMEText(body, _subtype="plain")
        message.attach(text_part)

        if attachment_path:
            filename = os.path.basename(attachment_path)

            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', _subtype='octet-stream')
                part.set_payload(attachment.read())

            encoders.encode_base64(part)

            part.add_header(
                'Content-Disposition',
                f'attachment; filename={filename}'
            )

            message.attach(part)

        try:
            context = ssl.create_default_context()

            with smtplib.SMTP(self.smtp_server, int(self.port)) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
                print('Email sent successfully')
        except Exception as e:
            print(f'Failed to send email: {e}')
