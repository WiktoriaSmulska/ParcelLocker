from src.converter import Converter, UserConverter, ParcelConverter, LockerConverter, DeliversConverter
from src.email_sender import EmailSender
from src.email_service import EmailService
from src.file_service import (
    UserJsonFileReader,
    ParcelJsonFileReader,
    LockerJsonFileReader,
    DeliverJsonFileReader,
    UserJsonFileWriter,
    ParcelJsonFileWriter,
    LockerJsonFileWriter,
    DeliverJsonFileWriter
)
from decimal import Decimal
from src.model import Lockers, Delivers, UserDataDict, ParcelsDataDict, Parcels, LockersDataDict, DeliversDataDict
from src.report_generate import ReportGenerator
from src.repository import UserDataRepository, ParcelDataRepository, LockerDataRepository, DeliverDataRepository
from src.service import PurchaseSummaryService
from src.speech_recognizer_service import SpeechRecognizerService

from src.validator import AbstractValidator
from src.model import LockerComponentsSize, City, Users
from datetime import date
from src.validator import UserDataDictValidator, LockerDataDictValidator, ParcelDataDictValidator, DeliverDataDictValidator
from datetime import date
import os
from dotenv import load_dotenv
from src.speech_recognizer import SpeechRecognizer
from src.speech_recognizer_service import SpeechRecognizerService
def main() -> None:
    lockers = {
        "L001": Lockers(
            locker_id="L001",
            city=City.NEW_YORK,
            latitude=40.730610,
            longitude=-73.935242,
            compartments={LockerComponentsSize.SMALL: 20, LockerComponentsSize.MEDIUM: 15, LockerComponentsSize.LARGE: 5}
        ),
        "L002": Lockers(
            locker_id="L002",
            city=City.LOS_ANGELES,
            latitude=34.052235,
            longitude=-118.243683,
            compartments={LockerComponentsSize.SMALL: 25, LockerComponentsSize.MEDIUM: 10, LockerComponentsSize.LARGE: 8}
        )
    }


    parcels = {
        "P12345": Parcels(parcel_id="P12345", height=30, length=50, weight=5),
        "P67890": Parcels(parcel_id="P67890", height=20, length=40, weight=4)
    }


    delivers = [
        Delivers(
            parcel_id="P12345",
            locker_id="L001",
            sender_email="alice.smith@example.com",
            receiver_email="john.doe@example.com",
            sent_date=date(2023, 12, 1),
            expected_delivery_date=date(2023, 12, 5)
        ),
        Delivers(
            parcel_id="P67890",
            locker_id="L002",
            sender_email="bob.jones@example.com",
            receiver_email="jane.smith@example.com",
            sent_date=date(2023, 12, 2),
            expected_delivery_date=date(2023, 12, 6)
        )
    ]
    users = {
        "john.doe@gmail.com": Users(
            email="john.doe@gmail.com",
            name="John",
            surname="Doe",
            city=City.NEW_YORK,
            latitude=40.712776,
            longitude=-74.005974
        ),
        "jane.smith@gmail.com": Users(
            email="jane.smith@gmail.com",
            name="Jane",
            surname="Smith",
            city=City.LOS_ANGELES,
            latitude=34.052235,
            longitude=-118.243683
        ),
        "alice.smith@gmail.com": Users(
            email="alice.smith@gmail.com",
            name="Alice",
            surname="Smith",
            city=City.CHICAGO,
            latitude=41.878113,
            longitude=-87.629799
        ),
        "bob.jones@gmail.com": Users(
            email="bob.jones@gmail.com",
            name="Bob",
            surname="Jones",
            city=City.SAN_FRANCISCO,
            latitude=37.774929,
            longitude=-122.419418
        )
    }

    user_reader = UserJsonFileReader()
    parcel_reader = ParcelJsonFileReader()
    locker_reader = LockerJsonFileReader()
    deliver_reader = DeliverJsonFileReader()

    user_validator = UserDataDictValidator()
    parcel_validator = ParcelDataDictValidator()
    locker_validator = LockerDataDictValidator()
    deliver_validator = DeliverDataDictValidator()


    user_converter = UserConverter()
    parcel_converter = ParcelConverter()
    locker_converter = LockerConverter()
    deliver_converter = DeliversConverter()


    user_repo = UserDataRepository(
        file_reader=user_reader,
        validator=user_validator,
        converter=user_converter,
        filename="data/users.json"
    )

    parcel_repo = ParcelDataRepository(
        file_reader=parcel_reader,
        validator=parcel_validator,
        converter=parcel_converter,
        filename="data/parcels.json"
    )

    locker_repo = LockerDataRepository(
        file_reader=locker_reader,
        validator=locker_validator,
        converter=locker_converter,
        filename="data/lockers.json"
    )

    deliver_repo = DeliverDataRepository(
        file_reader=deliver_reader,
        validator=deliver_validator,
        converter=deliver_converter,
        filename="data/delivers.json"
    )


    service = PurchaseSummaryService(
        locker_repo=locker_repo,
        user_repo=user_repo,
        parcel_repo=parcel_repo,
        deliver_repo=deliver_repo,
        lockers=lockers,
        parcels=parcels,
        delivers=delivers,
        users=users,
        locker_usage = {locker_id: {LockerComponentsSize.SMALL: 0, LockerComponentsSize.MEDIUM: 0, LockerComponentsSize.LARGE: 0} for locker_id in lockers}
    )


    #report_gen = ReportGenerator(service)
    #report_gen.generate_report("data/report.txt")

    # smtp_server = os.getenv('SMTP_SERVER')
    # port = int(os.getenv('PORT'))
    # sender_email = os.getenv('SENDER_EMAIL')
    # sender_password = os.getenv('SENDER_PASSWORD')

    #email_sender = EmailSender(smtp_server, port, sender_email, sender_password)

    # recipient_mail = 'wiktoriasmulska0@gmail.com'
    # subject = 'KM Test Email'
    # body = 'This is a test email with attachment.'
    # attachment_path = r'C:\Users\User\Desktop\proj\projects_python\projectt\data\report.txt'
    #em = EmailService(service)
    # em.generate_and_send_email(subject, body, attachment_path)
    #em.send_email_about_free_locker('alice.smith@gmail.com', parcels['P12345'])

    #email_sender.send_email(recipient_mail, subject, body, attachment_path)
    spr = SpeechRecognizerService(deliver_repo=deliver_repo)
    sp = SpeechRecognizer(spr)

    sp.handle_conversation()
if __name__ == '__main__':
    main()
