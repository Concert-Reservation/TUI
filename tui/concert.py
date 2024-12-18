class Concert:
    def __init__(self, id, name, description, start_date, end_date, price, seat_limit):
        self.id = id
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.price = price
        self.seat_limit = seat_limit

    def __str__(self):
        return f"{self.name} ({self.start_date} to {self.end_date})"