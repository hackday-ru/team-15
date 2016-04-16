from app.models import Event

class Debt:
    def __init__(self, user, debt):
        self.user = user
        self.debt = debt

class EventItem:
    def __init__(self):
        pass


def create_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
