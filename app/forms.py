from flask.ext.wtf import Form
from flask import g
from wtforms import StringField, BooleanField, SelectMultipleField, SelectField, widgets
from wtforms.validators import Required
from flask_openid import COMMON_PROVIDERS
from wtforms.widgets.core import HTMLString, html_params

class FuckingListWidget(object):
    """
    Renders a list of fields as a `ul` or `ol` list.

    This is used for fields which encapsulate many inner fields as subfields.
    The widget will try to iterate the field to get access to the subfields and
    call them to render them.

    If `prefix_label` is set, the subfield's label is printed before the field,
    otherwise afterwards. The latter is useful for iterating radios or
    checkboxes.
    """
    def __init__(self, html_tag='ul', prefix_label=True):
        assert html_tag in ('ol', 'ul')
        self.html_tag = html_tag
        self.prefix_label = prefix_label

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = ['<%s %s>' % (self.html_tag, html_params(**kwargs))]
        for subfield in field:
            if self.prefix_label:
                html.append('<li class="list-group-item">%s %s</li>' % (subfield.label, subfield()))
            else:
                html.append('<li class="list-group-item">%s %s</li>' % (subfield(), subfield.label))
        html.append('</%s>' % self.html_tag)
        return HTMLString(''.join(html))


class MultiCheckboxField(SelectMultipleField):
    widget = FuckingListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class LoginForm(Form):
    openid = StringField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)


class NewPartyForm(Form):
    name = StringField(u'Full Name')
    # name.field(class_ = 'form_control')
    #users = [(x.id, x.nickname) for x in g.user.get_friends()]
    # language = MultiCheckboxField()
    language = MultiCheckboxField(u'Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
