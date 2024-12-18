from unittest.mock import patch
from concert_reservation.menu import Menu, Description, Entry

def test_menu_creation():
    # Creazione del menu con un'uscita
    menu = Menu.Builder(Description("Test Menu")) \
        .with_entry(Entry.create("0", "Exit", is_exit=True)) \
        .build()

    assert menu is not None

def test_menu_entry_selection():
    # Mock a function called when an option is selected
    called = {"value": False}

    def on_selected():
        called["value"] = True

    # Build the menu using the Builder
    menu = Menu.Builder(Description("Test Menu")) \
        .with_entry(Entry.create("1", "Option 1", on_selected)) \
        .with_entry(Entry.create("0", "Exit", is_exit=True)) \
        .build()

    # Simulate selecting an option
    with patch("builtins.input", side_effect=["1", "0"]):  # Select "Option 1" then exit
        menu.run()

    # Assert the callback was called
    assert called["value"] is True
