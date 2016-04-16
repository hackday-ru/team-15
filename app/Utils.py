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
    from app import db
    event = Event(name, datetime.datetime.utcnow())
    db.session.add(event)
    db.session.flush()
    db.session.refresh(event)
    for participant in participants:
        db.session.add(Participant(participant, event.id))
    db.session.commit()