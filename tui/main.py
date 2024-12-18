import curses
import requests

# URL per django
API_URL = "http://localhost:8000/events/api/concerts/"
TICKET_URL = "http://localhost:8000/events/api/tickets/"

# GET REQUEST per django backend per restituire concerti
def fetch_concerts():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return []

# POST REQUEST per comprare un ticket
def buy_ticket(concert_id, user_id):
    ticket_data = {
        'user': user_id,
        'concert': concert_id
    }
    response = requests.post(TICKET_URL, data=ticket_data)
    return response.status_code == 201  # Return True if the ticket was bought successfully


def display_concerts(stdscr, concerts):
    stdscr.clear()
    stdscr.addstr(0, 0, "Available Concerts:")
    stdscr.addstr(1, 0, "-----------------------------------")

    for idx, concert in enumerate(concerts, 2):
        stdscr.addstr(idx, 0, f"{idx - 1}. {concert['name']} ({concert['start_date']})")

    stdscr.addstr(len(concerts) + 2, 0, "Enter concert number to buy ticket, or q to quit:")


def main(stdscr):
    # stdscr è lo schermo
    stdscr.clear()

    user_id = 1  # assumo che questo utente 1 ha fatto il login

    # Fetch concerts from the API
    concerts = fetch_concerts()
    if not concerts:
        stdscr.addstr("Failed to fetch concerts")
        stdscr.refresh()
        stdscr.getch() # termina premendo un tasto
        return

    display_concerts(stdscr, concerts)

    while True:
        stdscr.refresh()
        key = stdscr.getch() # attende che venga premuto un tasto

        if key == ord('q'):
            break

        # se viene premuto un tasto tra 1 e 9,
        if key in range(ord('1'), ord('9') + 1):
            concert_num = key - ord('1') # calcola indice del concerto
            if concert_num < len(concerts): # se concerto è valido, prendi l'id
                concert_id = concerts[concert_num]['id']
                success = buy_ticket(concert_id, user_id) # viene comprato il ticket
                if success:
                    stdscr.addstr(len(concerts) + 3, 0, f"Ticket bought for concert: {concerts[concert_num]['name']}")
                else:
                    stdscr.addstr(len(concerts) + 3, 0, "Failed to buy ticket. Try again.")
            else:
                stdscr.addstr(len(concerts) + 3, 0, "Invalid concert selection.")

            stdscr.refresh()
            stdscr.getch()
            display_concerts(stdscr, concerts)  # Redisplay the concert list


if __name__ == "__main__":
    curses.wrapper(main)

