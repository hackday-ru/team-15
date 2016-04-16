from flask.ext.wtf import Form
from flask import g
from app.models import User
from wtforms import StringField, BooleanField, SelectMultipleField, FloatField, SelectField, widgets
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


class NewPartyForm(Form):
    name = StringField(u'Full Name')
    users = [(g.user.id, "Я")] + [(x.User.id, x.User.nickname) for x in User.get_friends(g.user)]
    language = MultiCheckboxField(u'Friends', choices=users)


class NewItemForm(Form):
    goodName = StringField(u'Good Name')
    cost = FloatField(0)
    users = [(g.user.id, "Я")] + [(x.User.id, x.User.nickname) for x in User.get_friends(g.user)]
    language = MultiCheckboxField(u'Friends', choices=users)
