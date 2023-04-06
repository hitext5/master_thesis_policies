from dataclasses import dataclass


@dataclass
class SmokeDetector:
    smoke_detected: bool

    def get_smoke_detected(self):
        return self.smoke_detected

    def get_json_smoke_detected(self):
        return {"smoke_detected": self.smoke_detected}
