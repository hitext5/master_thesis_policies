from dataclasses import dataclass


@dataclass
class ElectronicDevice:
    work_power: int

    def get_work_power(self):
        return self.work_power
