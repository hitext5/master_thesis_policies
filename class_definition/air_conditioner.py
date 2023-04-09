from dataclasses import dataclass


@dataclass
class AirConditioner:
    turned_on: bool

    def get_ac_status(self):
        return self.turned_on

    def get_json_ac_status(self):
        return {"turned_on": self.turned_on}

    def set_ac_status(self, new_value):
        self.turned_on = new_value
