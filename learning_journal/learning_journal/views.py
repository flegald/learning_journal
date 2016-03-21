from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
import markdown
from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Entry,
    )

from .forms import EntryForm


@view_config(route_name='home', renderer='templates/list.jinja2')
def list_view(request):
    try:
        entries = DBSession.query(Entry).order_by(Entry.created.desc())
    except DBAPIError:
        return Response(conn_err_msg,
                        content_type='text/plain',
                        status_int=500)
    return {"entries": entries}


@view_config(route_name='single_entry', renderer='templates/single_entry.jinja2')
def single_entry_view(request):
    try:
        entry_id = request.matchdict['id']
        single_entry = DBSession.query(Entry).get(entry_id)
    except DBAPIError:
        return Response(conn_err_msg,
                        content_type='text/plain',
                        status_int=500)
    # NOTE: We used Jared and AJ's code as an example
    md = markdown.Markdown(safe_mode="replace", html_replacement_text="NO")
    text = md.convert(single_entry.text)
    return {"single_entry": single_entry, "text": text}


@view_config(route_name='add_entry', renderer='templates/add_entry.jinja2')
def add_entry_view(request):
    """Display an empty form for a new entry."""
    # 1. view to create new entry
    # 2. return user to single_entry_view(created_entry)

    # instantiate entry_form, populating it with data from request
    entry_form = EntryForm(request.POST)
    # if you got here from add_entry view with complete form -
    if request.method == 'POST' and entry_form.validate():
        entry = Entry(title=entry_form.title.data, text=entry_form.text.data)
        DBSession.add(entry)
        DBSession.flush()
        entry_id = entry.id  # NOTE: must use mediating symbol
        # go to detail view of that entry
        return HTTPFound(location='/entries/{}'.format(entry_id))
    # else if form not valid, return to add_entry_view WITH existing form info
    # if you did not get here from filled-out add-entry form
    # TODO: if not entry_form.validate(), add info to form indicating failure
    return {"form": entry_form}


# @view_config(route_name='edit_entry', renderer='templates/edit_entry.jinja2')
# def edit_entry_view(request):
#     entry_id = request.matchdict['id']
#     entry_record = DBSession.query(Entry).get(entry_id)
#     entry_form = EntryForm(request.POST, entry_record)  # magical form populating
#     if request.method == 'POST' and entry_form.validate():
#         entry_form.populate_obj(entry_record)  # this mutates entry_record, not entry_form!!
#         entry_id = entry_record.id
#         return HTTPFound(location='/entries/{}'.format(entry_id))
#     return {'form': entry_form}


@view_config(route_name="edit_entry", renderer='templates/edit_entry.jinja2')
def edit_entry_view(request):
    """"""
    entry_form = EntryForm(request.POST)
    entry_id = request.matchdict['id']
    # grab record from db to populate fields
    entry_record = DBSession.query(Entry).get(entry_id)
    # if you got here from edit_entry view with valid form:
    if request.method == 'POST' and entry_form.validate():
        # overwrite record with incoming request form data
        # NOTE: could use entry_form.populate_obj(entry_record), but this is clearer
        # entry_record.title = entry_form.title.data
        # entry_record.text = entry_form.text.data
        entry_form.populate_obj(entry_record)
        entry_id = entry_record.id  # NOTE: must use mediating symbol
        # commit changed entry into db
        # DBSession.flush()  # is this done implicitly because sqlalchemy knows it's 'dirty'??
        # send user to detail view of given entry, reflecting changes
        return HTTPFound(location='/entries/{}'.format(entry_id))
    # if you did not get here from edit_entry view:
    else:
        # do i need to touch my existing entry_form object before returning?
        # yes, you need to put text, title from record into form
        entry_form = EntryForm(request.POST, entry_record)  # wtforms automagically knows what to do with entry_record??
        # entry_form.title.data = entry_record.title
        # entry_form.text.data = entry_record.text
        return {'form': entry_form}
    # 1. Display form poplated with values from existing entry
    # 2. view will update existing values when submitted
    # form must accept markdown


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

