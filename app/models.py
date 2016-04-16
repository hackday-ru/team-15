from app import db

ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    def __init__(self, id1, nickname, email):
        self.id = id1
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


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    date = db.Column(db.DateTime)


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('item.id'))


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    cost = db.Column(db.Integer)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))


class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
