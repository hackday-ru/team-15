from app.models import Event, Participant
import datetime
from sqlalchemy.sql import func

class Debt:
    def __init__(self, user, debt):
        self.user = user
        self.debt = debt

class EventItem:
    def __init__(self):
        pass


def build_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    return event

def create_event(name, participants):
    event = Event(name, datetime.datetime.utcnow())
    for participant in participants:
        Participant(participant, event.id)