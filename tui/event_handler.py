import requests

from concert import Concert
from ticket import Ticket

class EventHandler:
    def __init__(self):
        self.concerts = []
        self.tickets = []
        self.ticket_id_counter = 1

    def create_concert(self, concert):
        self.concerts.append(concert)
        print(f"Concert '{concert.name}' created successfully")

    def remove_concert(self, concert_id):
        self.concerts = [c for c in self.concerts if c.id != concert_id]
        print(f"Concert with ID {concert_id} removed successfully")

    def buy_ticket(self, user_id, concert_id):
        if not any(c.id == concert_id for c in self.concerts):
            print("Concert not found")
            return
        ticket = Ticket(self.ticket_id_counter, user_id, concert_id)
        self.tickets.append(ticket)
        self.ticket_id_counter += 1
        print("Ticket bought successfully")

