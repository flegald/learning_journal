import pytest
from pyramid import testing
from .conftest import dbtransaction
from .conftest import DBSession
from ..views import (list_view, single_entry_view)
from ..models import Entry

ENTRIES = [
    ('title 1', 'text 1'),
    ('title 2', 'text 2'),
]


# def test_list(loaded_db):
#     return_dict = list_view(req)
#     print(return_dict['entries'].title)
#     # assert return_dict['entries'].title == "my_second_entry "
#     # assert list(req) == {}


@pytest.mark.parametrize(('title', 'text'), ENTRIES)
def test_entry_view_text(title, text, dbtransaction):
    """Test for entry view dictionary text attribute."""
    entry = Entry(title=title, text=text)
    DBSession.add(entry)
    DBSession.flush()
    req = testing.DummyRequest()
    req.matchdict = {'id': entry.id}
    dic = list_view(req)
    # TODO: test both attributes in one assert statement
    # NOTE: for attribute in [text, title] does not work
    assert dic['entries'][0].text == text
    assert dic['entries'][0].title == title
