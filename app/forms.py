from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import Required

class LoginForm(Form):
    openid = StringField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)
