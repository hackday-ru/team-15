from app.models import Event, Participant, Item, User, Customers
import datetime
from sqlalchemy.sql import func

class Debt:
    def __init__(self, user, debt):
        self.user = user
        self.debt = debt


class EventItem:
    def __init__(self, name1, cost1, owner1, ls, ss, id1):
        #todo pass id's
        self.id = id1
        self.name = name1
        self.cost = cost1
        self.owner = owner1
        self.small_repr = ss
        self.full_repr = ls

def build_event(event_id):
    from app import db
    event = Event.query.filter_by(id=event_id).first()
    if event is None:
        return None
    items = db.session.query(Item, User).filter(Item.event_id == event_id).filter(Item.owner == User.id).all()
    customers = db.session.query(Item, Customers, User).filter(Item.event_id == event_id).filter(Customers.item_id == Item.id).filter(Customers.user_id == User.id).all()
    res = []
    for item in items:
        parts = [x.User.nickname for x in customers if x.Item.id == item.Item.id]
        large_s = ", ".join(parts)
        small_s = large_s[:7] + "..."
        res.append(EventItem(item.Item.name, item.Item.cost, item.User, large_s, small_s, item.Item.id))

    return res

def create_event(name, participants):
    from app import db
    event = Event(name, datetime.datetime.utcnow())
    db.session.add(event)
    db.session.flush()
    db.session.refresh(event)
    for participant in participants:
        db.session.add(Participant(participant, event.id))
    db.session.commit()