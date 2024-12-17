from dataclasses import dataclass
from typeguard import typechecked
from .validators import validate_dataclass, validate

@typechecked
@dataclass(frozen=True, order=True)
class Reservation:
    Date: str
    Concert: str
    User: str
    Seat: int

    def __post_init__(self):
        validate_dataclass(self)
        validate(self)

    def __str__(self):
        return f"{self.Date} {self.Concert} {self.User} {self.Seat}"
