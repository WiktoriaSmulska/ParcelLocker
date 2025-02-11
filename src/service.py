from collections import Counter
from dataclasses import dataclass
from src.model import (
    Delivers,
    Users,
    Parcels,
    Lockers,
    LockerComponentsSize,
    City, UserDataDict,

    UserDataDict,
    ParcelsDataDict,
    LockersDataDict,
    DeliversDataDict
)
from src.repository import PurchaseSummaryRepository, UsersWithPurchaseDelivers, AbstractDataRepository
from geopy.distance import geodesic # type: ignore[import]

from tests.model.conftest import parcels, delivers
import logging



logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

@dataclass
class PurchaseSummaryService:
    locker_repo: AbstractDataRepository
    user_repo: AbstractDataRepository
    parcel_repo: AbstractDataRepository
    deliver_repo: AbstractDataRepository

    lockers: dict[str, Lockers]
    parcels: dict[str, Parcels]
    delivers: list[Delivers]
    users: dict[str, Users]
    locker_usage: dict[str, dict]

    def __post_init__(self)->None:
        self.lockers = {locker.locker_id: locker for locker in self.locker_repo.get_data()}
        self.parcels = {parcel.parcel_id: parcel for parcel in self.parcel_repo.get_data()}
        self.delivers = self.deliver_repo.get_data()
        self.users = {user.email: user for user in self.user_repo.get_data()}
        self.locker_usage = {locker_id: {LockerComponentsSize.SMALL: 0, LockerComponentsSize.MEDIUM: 0, LockerComponentsSize.LARGE: 0} for locker_id in self.lockers}

    def get_parcel_size(self, parcel: Parcels)->LockerComponentsSize:
        if parcel.height <= 10 and parcel.length <= 20:
            return LockerComponentsSize.SMALL
        elif parcel.height <= 30 and parcel.length <= 50:
            return LockerComponentsSize.MEDIUM
        else:
            return LockerComponentsSize.LARGE

    def check_locker_capacity(self)->None:

        for deliver in self.delivers:
            parcel = self.parcels.get(deliver.parcel_id)
            locker_id = deliver.locker_id

            if parcel:
                size = self.get_parcel_size(parcel)
                self.locker_usage[locker_id][size] += 1

            for locker_id, usage in self.locker_usage.items():
                locker = self.lockers[locker_id]

                for size, num in usage.items():
                    max_capacity = locker.compartments[size]
                    if num > max_capacity:
                        logging.error(
                        f"Locker {locker_id} exceeded capacity for {size} parcels. "
                        f"Used: {num}, Capacity: {max_capacity}"
                        )


    def most_often_used_size_of_parcel(self)->dict[str, list[int]]:
        most_popular_sizes = {}
        for deliver in self.delivers:
            locker_id = deliver.locker_id
            parcel = self.parcels.get(deliver.parcel_id)


            if parcel is not None:
                size = self.get_parcel_size(parcel)
                self.locker_usage[locker_id][size] += 1


        for locker_id, dict_of_size in self.locker_usage.items():
            most_popular_size = max(dict_of_size.values())
            most_popular_sizes[locker_id] = [size for size, count in dict_of_size.items() if count == most_popular_size]

        return most_popular_sizes


    def person_who_sended_and_picked_up_packages(self, how_many: int):
        senders: Counter[str] = Counter()
        receivers: Counter[str]  = Counter()


        for deliver in self.delivers:
            senders[deliver.sender_email] += 1
            receivers[deliver.receiver_email] += 1

        sorted_senders = dict(senders.most_common(how_many))
        sorted_receivers = dict(receivers.most_common(how_many))
        # print("++++++++++++++++++")
        # print(sorted_senders)
        # print("++++++++++++++++++")
        farthest_senders = self.find_farthest_users(sorted_senders)
        farthest_receivers = self.find_farthest_users(sorted_receivers)
        # print("++++++++++++++++++")//nic
        # print(farthest_senders)
        # print("++++++++++++++++++")
        return farthest_senders, farthest_receivers

    def find_farthest_users(self, top_users: dict[str, int]):
        farthest_users = {}

        for user_email, _ in top_users.items():
            user = self.users.get(user_email)
            if user:
                user_location = (user.latitude, user.longitude)

                max_distance = 0
                farthest_locker = None

                for locker_id, locker in self.lockers.items():
                    locker_location = (locker.latitude, locker.longitude)
                    distance = geodesic(user_location, locker_location).kilometers

                    if distance > max_distance:
                        max_distance = distance
                        farthest_locker = locker_id

                farthest_users[user_email] = {
                    "farthest_locker": farthest_locker,
                    "max_distance": max_distance,
                }
            else:
                logging.warning(f"No user found with email {user_email}. Skipping...")

        return farthest_users

    def longest_delivery(self):
        senders = {}
        for deliver in self.delivers:
            sender = deliver.sender_email
            #logging.debug(sender)
            delivery_duration = (deliver.expected_delivery_date - deliver.sent_date).days

            if sender not in senders:
                senders[sender] = []

            senders[sender].append(delivery_duration)
            logging.debug(senders)

        longest_deliveries = {sender: max(days) for sender, days in senders.items()}
        max_sender = max(longest_deliveries, key=lambda s: longest_deliveries[s])
        longest_time = longest_deliveries[max_sender]
        #logging.debug("++++")
        #logging.debug(max_sender)
        #logging.debug(longest_time)
        return max_sender, longest_time