from dataclasses import dataclass
from datetime import datetime, time


# Could be an Amazon Echo Dot or another multipurpose device
@dataclass
class Clock:
    current_time: time.hour

    def get_current_time(self):
        return self.current_time

    def get_json_current_time(self):
        return {"current_time": self.current_time}

    def update_time(self):
        self.current_time = datetime.now().hour
