from pyramid.response import Response
from pyramid.view import view_config

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
        single_entry = DBSession.query(Entry).filter_by(id=request.matchdict['id']).first()
    except DBAPIError:
        return Response(conn_err_msg,
                        content_type='text/plain',
                        status_int=500)
    return {"single_entry": single_entry}


@view_config(route_name='add_entry', renderer='templates/add_entry.jinja2')
def add_entry_view(request):
    """Display an empty form for a new entry."""
    # 1. view to create new entry
    # 2. return user to single_entry_view(created_entry)

    # instantiate entry_form, populating it with data from request
    entry_form = EntryForm(request.POST)
    if request.method == 'POST' and entry_form.validate():
        # instantiate entry db record object, populating it from entry_form object
        entry = Entry(title=entry_form.title, text=entry_form.text)
        DBSession.add(entry) # do i need to DBSession.flush() ?? probably not.
        redirect('register')  # TODO: translate to pyramid-ese
    # else if form not valid, return to add_entry_view WITH existing form info
    # ok, apparently we are passing a FORM object to the renderer
    return {"form": entry_form} #  render_response('register.html', form=form) # TODO: what is this??


@view_config(route_name="edit_entry", renderer='templates/edit_entry.jinja2')
def edit_entry_view(request):
    """"""
    # 1. Display form poplated with values from existing entry
    # 2. view will update existing values when submitted
    # form must accept markdown

#################################
########## example from wtforms

#   user = request.current_user  # name the user passed in by the request
#   form = ProfileForm(request.POST, user)  # instantiate a new form object, populated with request attributes
#   if request.method == 'POST' and form.validate():
#       form.populate_obj(user)  # isn't the form already populated with the user??
#       user.save()  # why does user have a .save() method?
#                    # it's the user from the request originally passed in
#                    # did the *request* pass in a user *object* ??
#       redirect('edit_profile')
#   return render_response('edit_profile.html', form=form)

##################################

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

