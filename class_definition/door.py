from dataclasses import dataclass


@dataclass
class Door:
    closed_state: bool

    def get_closed_state(self):
        return self.closed_state

    def set_closed_state(self, new_value):
        self.closed_state = new_value
