from app.models import Event, Participant, Item, User, Friends, Customers
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


def create_item(name, cost, event_id, owner, participants):
    from app import db
    average_cost = int(int(cost * 100) / len(participants))
    for p in participants:

        if int(p) == owner.id:
            continue

        friend = Friends.query.filter_by(user_id=owner.id, friend_id=int(p)).first()
        if friend.debt is None:
            friend.debt = 0
        friend.debt += average_cost
        db.session.commit()

        friend = Friends.query.filter_by(user_id=int(p), friend_id=owner.id).first()
        if friend.debt is None:
            friend.debt = 0
        friend.debt -= average_cost
        db.session.commit()

    item = Item(name, cost, event_id, owner.id)
    db.session.add(item)
    db.session.flush()
    db.session.refresh(item)
    for participant in participants:
        db.session.add(Customers(item.id, participant))
    db.session.commit()

class Expenses:
    def __init__(self, items):
        self.names = [x.name for x in items]
        self.costs = [x.cost for x in items]


class SpentOrAte:
    def __init__(self, names1, paid1, ate1):
        self.names = names1
        self.paid = paid1
        self.ate = ate1


def create_stats(event_id):
    from app import db
    items = Item.query.filter_by(event_id=event_id).all()
    q = db.session.query(Item, Customers, User).filter(Item.event_id==event_id).filter(Customers.item_id==Item.id).filter(User.id == Customers.user_id);

    from collections import defaultdict
    itemCount = defaultdict(int)
    for query in q:
        itemCount[query.Item.id] += 1

    ate = defaultdict(int)
    paid = defaultdict(int)
    for query in q:
        ate[query.User.id] += int(query.Item.cost/itemCount[query.Item.id])

    for item in items:
        paid[item.owner] += item.cost

    names = {(query.User.id, query.User.nickname) for query in q}
    names1 = []
    paid1 = []
    ate1 = []
    for (id, name) in list(names):
        names1.append(name)
        paid1.append(paid[id])
        ate1.append(ate[id])
    return SpentOrAte(names1, paid1, ate1)


