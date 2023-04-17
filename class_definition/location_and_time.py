from dataclasses import dataclass

from clock import Clock
from owner_location import ApartmentOwner


@dataclass
class LocationAndTime:
    apartment_owner: ApartmentOwner
    clock: Clock
