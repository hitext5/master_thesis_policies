from dataclasses import dataclass


@dataclass
class ApartmentOwner:
    at_home: bool

    def get_location(self):
        return self.at_home

    def get_json_location(self):
        return {"at_home": self.at_home}

    def set_location(self, new_value):
        self.at_home = new_value
