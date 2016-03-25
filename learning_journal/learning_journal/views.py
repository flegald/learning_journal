"""View Handeling."""
import os
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, forbidden_view_config
import markdown
from sqlalchemy.exc import DBAPIError
from pyramid.security import remember, forget
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from security import USERS, check_pw
from .models import (
    DBSession,
    Entry,
    )

from .forms import EntryForm, LoginForm


@view_config(route_name='home',
            renderer='templates/index.jinja2',
            permission="view")
def list_view(request):
    """Show the homepage."""
    try:
        entries = DBSession.query(Entry).order_by(Entry.created.desc())
    except DBAPIError:
        return Response(conn_err_msg,
                        content_type='text/plain',
                        status_int=500)
    return {"entries": entries}


@view_config(route_name='single_entry',
            renderer='templates/individual.jinja2',
            permission="view")
def single_entry_view(request):
    """Display the details of a single entry."""
    try:
        entry_id = request.matchdict['id']
        single_entry = DBSession.query(Entry).get(entry_id)
    except DBAPIError:
        return Response(conn_err_msg,
                        content_type='text/plain',
                        status_int=500)
    md = markdown.Markdown(safe_mode="replace", html_replacement_text="NO")
    text = md.convert(single_entry.text)
    return {"single_entry": single_entry, "text": text}


@view_config(route_name='add_entry',
            renderer='templates/add_entry.jinja2',
            permission="edit")
def add_entry_view(request):
    """Display an empty form for a new entry."""
    entry_form = EntryForm(request.POST)
    if request.method == 'POST' and entry_form.validate():
        entry = Entry(title=entry_form.title.data, text=entry_form.text.data)
        DBSession.add(entry)
        DBSession.flush()
        entry_id = entry.id
        return HTTPFound(location='/entries/{}'.format(entry_id))
    return {"form": entry_form}


@view_config(route_name="edit_entry",
            renderer='templates/edit.jinja2',
            permission="edit")
def edit_entry_view(request):
    """Display for to edit existing entry."""
    entry_form = EntryForm(request.POST)
    entry_id = request.matchdict['id']
    entry_record = DBSession.query(Entry).get(entry_id)
    if request.method == 'POST' and entry_form.validate():
        entry_form.populate_obj(entry_record)
        entry_id = entry_record.id
        return HTTPFound(location='/entries/{}'.format(entry_id))
    else:
        entry_form = EntryForm(request.POST, entry_record)
        return {'form': entry_form}


@view_config(route_name='login', renderer='templates/login.jinja2')
@forbidden_view_config(renderer="templates/login.jinja2")
def login_view(request):
    """Handle log in."""
    login_form = LoginForm(request.POST)
    if request.method == "GET":
        action_head = "Please Login"
        return {'form': login_form, 'action_head': action_head}
    elif request.method == "POST":
        login = login_form.username.data
        password = login_form.password.data
        if check_pw(login, password):
            headers = remember(request, login)
            return HTTPFound(location="/", headers=headers)
        else:
            action_head = "Login Failed"
            login_form.password = ""
            return {"form": login_form, 'action_head': action_head}


@view_config(route_name='logout',
            renderer="/",
             permission='view')
def logout_view(request):
    """Logout function."""
    headers = forget(request)
    return HTTPFound(location="/",
                     headers=headers)

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_learning_journal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

