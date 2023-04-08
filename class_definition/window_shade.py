from dataclasses import dataclass


@dataclass
class WindowShade:
    closed_state: bool

    def get_closed_state(self):
        return self.closed_state

    def get_json_closed_state(self):
        return {"closed_state": self.closed_state}

    def set_closed_state(self, new_value):
        self.closed_state = new_value
