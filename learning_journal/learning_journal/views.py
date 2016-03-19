from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError


from .models import (
    DBSession,
    Entry,
    )


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

