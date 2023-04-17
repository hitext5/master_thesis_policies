from dataclasses import dataclass


@dataclass
class Door:
    locked: bool

    def get_closed_state(self):
        return self.locked

    def set_closed_state(self, new_value):
        self.locked = new_value
