from flask.ext.wtf import Form
from flask import g
from wtforms import TextField, BooleanField, SelectMultipleField, SelectField
from wtforms.validators import Required
from flask_openid import COMMON_PROVIDERS

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)


class NewPartyForm(Form):
    name    = TextField(u'Full Name', validators = [Required()])
    #users = [(x.id, x.nickname) for x in g.user.get_friends()]
    language = SelectMultipleField(u'Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
