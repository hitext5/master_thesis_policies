from dataclasses import dataclass

from door import Door
from light_bulb import LightBulb


@dataclass
class LightAndDoor:
    door: Door
    light_bulb: LightBulb
