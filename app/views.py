from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from app.forms import LoginForm
from app.models import User, ROLE_USER, ROLE_ADMIN

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    
@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('events'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.html', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('events'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))



class Debt:
    def __init__(self, user, debt):
        self.user = user
        self.debt = debt

@app.route('/')
@app.route('/user')
@login_required
def getUser():
    user = g.user
    return render_template('user.html',
        user=user, debts=[Debt(user=("user" + str(x)), debt=x*100) for x in range(10)])

@app.route('/events')
@login_required
def events():
    user = g.user
    return render_template('events.html',
        title = 'События',
        user = user)

@app.route('/')
@app.route('/event')
@login_required
def getEvent():
    user = g.user
    return render_template('event.html',
        user=user)

@app.route('/event_stats')
@login_required
def getEventStats():
    user = g.user
    return render_template('event_stats.html',
        user=user)

@app.route('/')
@app.route('/friends')
@login_required
def getFriends():
    user = g.user
    return render_template('friends.html',
        user=user)
