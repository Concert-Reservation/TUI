import pytest

from concert_reservation.domain import *


#Da cambiare, concert e reservation invertiti
def test_add_concert():
    reservation = Reservation()
    concert = Concert(Id(1), Client(2), Title("Concert1"), Date("2024-10-10"))

    reservation.add_concert(concert)
    assert reservation.number_of_concerts == 1
    assert reservation.concert_at_index(0) == concert

def test_concert_at_index():
    reservation = Reservation()
    concert1 = Concert(Id(2), Client(2), Title("Concert2"), Date("2024-10-11"))
    concert2 = Concert(Id(3), Client(3), Title("Concert4"), Date("2024-10-12"))

    reservation.add_concert(concert1)
    reservation.add_concert(concert2)

    assert reservation.concert_at_index(0) == concert1
    assert reservation.concert_at_index(1) == concert2


def test_number_of_concerts():
    reservation = Reservation()
    assert reservation.number_of_concerts == 0

    concert1 = Concert(Id(1), Client(2), Title("Concert1"), Date("2024-10-10"))
    reservation.add_concert(concert1)
    assert reservation.number_of_concerts == 1

def test_add_duplicate_concerts():
    reservation = Reservation()
    concert = Concert(Id(1), Client(2), Title("Concert1"), Date("2024-10-10"))

    reservation.add_concert(concert)
    reservation.add_concert(concert)

    assert reservation.number_of_concerts == 2
    assert reservation.concert_at_index(0) == concert
    assert reservation.concert_at_index(1) == concert


def test_reservation_with_large_data():
    reservation = Reservation()
    for i in range(1000):
        concert = Concert(id=Id(i + 1), title=Title(f"Concert {i + 1}"), date=Date("2024-05-01"), client=Client(i + 1))
        reservation.add_concert(concert)

    assert reservation.number_of_concerts == 1000
    assert reservation.concert_at_index(999).title.value == "Concert 1000"

