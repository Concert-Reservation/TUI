class Ticket:
    def __init__(self, id, id_user, id_concert):
        self.id = id
        self.id_user = id_user
        self.id_concert = id_concert

    def __str__(self):
        return f"Ticket for concert {self.id_concert} (User: {self.id_user})"