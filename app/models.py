
from sqlalchemy import UniqueConstraint
from app import db

ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    def __init__(self, nickname, email):
        self.nickname = nickname
        self.email = email

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.nickname

    @staticmethod
    def get_friends(user):
        return db.session.query(User, Friends).filter(user.id == Friends.user_id) \
            .filter(User.id == Friends.friend_id).all()


class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    debt = db.Column(db.Integer)
    __table_args__ = (UniqueConstraint('user_id', 'friend_id', name='_user_friend_uc'),)


class Event(db.Model):

    def __init__(self, name1, date1):
        self.name = name1
        self.date = date1

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    date = db.Column(db.DateTime)


class Participant(db.Model):

    def __init__(self, user_id1, event_id1):
        self.user_id = user_id1
        self.event_id = event_id1

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    __table_args__ = (UniqueConstraint('event_id', 'user_id', name='_user_event_uc'),)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    cost = db.Column(db.Integer)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))


class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    __table_args__ = (UniqueConstraint('item_id', 'user_id', name='_user_item_uc'),)
