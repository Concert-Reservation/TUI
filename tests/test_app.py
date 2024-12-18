from pathlib import Path
from unittest.mock import patch, mock_open, Mock

import pytest

from concert_reservation.domain import *

@pytest.fixture
def mock_path():
    Path.exists = Mock()
    Path.exists.return_value = True
    return Path

@pytest.fixture
def data():
    data = [
        ['author 1', 'title 1', 'i like very much this songs','rock','Milan', '2024-10-10', '2024-10-10', 8],
        ['author 2', 'title 2', 'i love very much this ','pop','Rome', '2024-10-10', '2024-10-10', 9],
        ['author 3', 'title 3', 'i like very much this artist','jazz','Naples', '2024-10-10', '2024-10-10', 10],
    ]
    return '\n'.join(['\t'.join(d) for d in data])

def assert_in_output(mocked_print, expected):
    mock_calls = '\n'.join([''.join(mock_call.args) for mock_call in mocked_print.mock_calls])
    assert expected.strip() in mock_calls


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_main(mocked_print, mocked_input):
    with patch.object(Path, 'exists') as mocked_path_exists:
        mocked_path_exists.return_value = False
        with patch('builtins.open', mock_open()):
            main('__main__')
            mocked_print.assert_any_call('*** Concert Reservation 2024 ***')
            mocked_print.assert_any_call('0:\tExit')
            mocked_print.assert_any_call('Bye!')
            mocked_input.assert_called()



















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

