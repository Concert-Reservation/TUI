from event_handler import EventHandler
from concert import Concert

handler = EventHandler()

def main():
    print("Creating a concert...")
    concert = Concert(1, "Sanremo", "concerto", "2024-10-10", "2024-10-02", 50, 100)
    handler.create_concert(concert)

    print("\nBuying a ticket...")
    handler.buy_ticket(user_id=1, concert_id=1)

if __name__ == "__main__":
    main()
