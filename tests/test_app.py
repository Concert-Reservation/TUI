from pathlib import Path
from unittest.mock import patch, mock_open, Mock
from  concert_reservation.__main__ import main

import pytest

from concert_reservation.app import App
from concert_reservation.domain import *

@pytest.fixture #indica che è una funzione di setup
def mock_path():
    Path.exists = Mock()
    Path.exists.return_value = True
    return Path



@patch('builtins.input', side_effect=['1', 'author', 'title', 'genre', '1:11', '0'])
@patch('builtins.print')
def test_app_add_song(mocked_print, mocked_input, mock_path):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    assert list(filter(lambda x: 'author' in str(x), mocked_print.mock_calls))

    handle = mocked_open()
    handle.write.assert_called_once_with('author\ttitle\tgenre\t1:11\n')
    mocked_input.assert_called()




'''
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
            mocked_print.assert_any_call('*** Concert Review 2024 ***')
            mocked_print.assert_any_call('0:\tExit')
            mocked_print.assert_any_call('Bye!')
            mocked_input.assert_called()

@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_load_datafile(mocked_print, mocked_input, mock_path, data):
    with patch('builtins.open', mock_open(read_data=data)):
        App().run()
    mock_path.exists.assert_called_once()
    assert_in_output(mocked_print, 'author 1')
    mocked_input.assert_called()

@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_handles_corrupted_datafile(mocked_print, mocked_input, mock_path):
    with patch('builtins.open', mock_open(read_data='xyz')):
        App().run()
    mocked_print.assert_any_call('Continuing with an empty dataset...')
    mocked_input.assert_called()
'''
