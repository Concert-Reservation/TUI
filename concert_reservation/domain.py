import re
from dataclasses import dataclass, InitVar, field
from typing import Any

from typeguard import typechecked
from valid8 import validate

from validation.dataclasses import validate_dataclass
from validation.regex import pattern
import datetime


@dataclass(frozen=True, order=True)
class Id:
    value: int

    def __post_init__(self):
        validate_dataclass(self)
        validate(
            'value',
            self.value,
            min_value=1,  # Assicurati che l'ID sia almeno 1 (ad esempio, per escludere valori negativi o zero)
            max_value=10**9  # Limite massimo personalizzabile (es. 1 miliardo)
        )

    def __str__(self):
        return str(self.value)


@dataclass(frozen=True, order=True)
class Date:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate(
            'value',
            self.value,
            custom=pattern(r'^\d{4}-\d{2}-\d{2}$')  # Formato ISO 8601: YYYY-MM-DD
        )

    def __str__(self):
        return self.value



@dataclass(frozen=True, order=True)
class Client:
    value: int

    def __post_init__(self):
        validate_dataclass(self)
        validate(
            'value',
            self.value,
            min_value=1,  # Assicurati che il client abbia un valore minimo (ad esempio, maggiore di 0)
            max_value=10**9  # Limite massimo personalizzabile per l'ID del cliente
        )

    def __str__(self):
        return str(self.value)


@dataclass(frozen=True, order=True)
class Title:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=100, custom=pattern(r'[0-9A-Za-z\s/-]*'))

    def __str__(self):
        return self.value


@dataclass(frozen=True, order=True)
class Reservation:
    id: Id
    title: Title
    client: Client
    date: Date

    def __post_init__(self):
        validate_dataclass(self)



@dataclass(frozen=True, order=True)
class Concert:
    __reservation: list[Reservation] = field(default_factory=list, init=False)
    id: Id
    client: Client
    title: Title
    date: Date


    def __post_init__(self):
        validate_dataclass(self) #da rivedere obv

    @property
    def number_of_reservation(self) -> int:
        return len(self.__reservation)

    def reservation_at_index(self, index: int) -> Reservation:
        return self.__reservation[index]

    def reservation_by_user(self, user: Client) -> list[Reservation]:
        return list(filter(lambda x: x.client == user, self.__reservation))

    def add_reservation(self, reservation: Reservation) -> None:
        self.__reservation.append(reservation)

    def remove_reservation(self, reservation: Reservation) -> None:
        self.__reservation.remove(reservation)



@dataclass(frozen=True, order=True)
class Genre:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=100, custom=pattern(r'Funk,Rock,Metal,Pop,Hip Hop,Country,Blues,Jazz'))

    def __str__(self):
        return self.value

    def __str__(self):
        return self.title


@dataclass(frozen=True, order=True)
class Content:
    body: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('body', self.body, min_len=1, max_len=1000, custom=pattern(r'^[\w\s.:;\'"]*$'))

    def __str__(self):
        return self.value

    def __str__(self):
        return self.title
