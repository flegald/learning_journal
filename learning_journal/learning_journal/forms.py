"""Define form classes"""

from wtforms import Form, StringField, validators


class EntryForm(Form):
    title = StringField('Title', [validators.Length(min=4, max=25)])
    text = StringField('Text', [validators.Length(min=6)])
