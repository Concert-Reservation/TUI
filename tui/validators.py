def validate_dataclass(instance):
    # Aggiungi validazioni per i campi del dataclass
    if not isinstance(instance.Date, str):
        raise ValueError("Date deve essere una stringa valida.")

def validate(instance):
    # Altre validazioni specifiche per la classe Reservation
    if instance.Seat <= 0:
        raise ValueError("Seat deve essere maggiore di 0.")
