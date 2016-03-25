"""Define form classes."""

from wtforms import Form, StringField, validators


class EntryForm(Form):
    """Create edit/create Entry form."""

    title = StringField('Title', [validators.Length(min=4, max=25)])
    text = StringField('Text', [validators.Length(min=6)])


class LoginForm(Form):
    """Create log in form."""

    username = StringField("Username", [validators.Length(min=4, max=25)])
    password = StringField("Password", [validators.Length(min=6)])
