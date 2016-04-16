from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from app import app, db, lm, oid
from app.models import User, Event, Participant, Friends, Item, Customers, ROLE_USER
import json

from app.Utils import Debt, EventItem, build_event, create_event

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('events'))
    from app.forms import LoginForm
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('events'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
def index():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('events'))

    return render_template('index.html')



@app.route('/user')
@login_required
def getUser():
    user = g.user
    return render_template('user.html',
                           user=user,
                           debts=[Debt(user=("user" + str(x)), debt=x * 100) for
                                  x in range(10)])


@app.route('/events', methods=['GET', 'POST'])
@login_required
def events():
    from app.users_forms import NewPartyForm
    form = NewPartyForm()
    if form.is_submitted():
        create_event(form.data['name'], form.data['language'])

    user = g.user
    q = db.session.query(User, Event, Participant).filter(
        User.email == user.email). \
        filter(Event.id == Participant.event_id). \
        filter(User.id == Participant.user_id).all()
    return render_template('events.html',
                           title='События',
                           user=user,
                           events=[x.Event for x in q], form=form)


@app.route('/event/<int:page>')
@login_required
def getEvent(page):
    from app.users_forms import NewItemForm
    form = NewItemForm()
    user = g.user
    res = build_event(page)
    if res is None:
        return render_template('404.html') #TODO 404
    else:
        return render_template('event.html',user=user, entries=res, form=form, page=page)


@app.route('/event_stats')
@login_required
def getEventStats():
    user = g.user
    return render_template('event_stats.html',
                           user=user)


@app.route("/items/delete", methods=['POST'])
@login_required
def delete_items():
    ids = json.loads(request.form["data"])
    for id1 in ids:
        Customers.query.filter_by(item_id=id1).delete()
        Item.query.filter_by(id=id1).delete()
    db.session.commit()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/friends')
@login_required
def get_friends():
    user = g.user
    q = User.get_friends(user)
    return render_template('friends.html',
                           user=user,
                           friends=[x.User for x in q])


@app.route("/friends/delete", methods=['POST'])
@login_required
def delete_friends():
    ids = json.loads(request.form["data"])
    for id1 in ids:
        Friends.query.filter_by(user_id=g.user.id, friend_id=int(id1)).delete()
    db.session.commit()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/friends/add", methods=['POST'])
@login_required
def add_friends():
    user = g.user
    name = json.loads(request.form["data"])
    q = User.query.filter(User.nickname.like("%" + name + "%")).all()
    for f in q:
        new_friend = Friends(user_id=user.id, friend_id=f.id)
        db.session.add(new_friend)
        new_friend = Friends(user_id=f.id, friend_id=user.id)
        db.session.add(new_friend)
        db.session.commit()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/404')
def getError():
    user = g.user
    return render_template('404.html',
                           user=user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
