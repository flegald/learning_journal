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


# TODO: understand this
# def test_list(loaded_db):
#     return_dict = list_view(req)
#     print(return_dict['entries'].title)
#     # assert return_dict['entries'].title == "my_second_entry "
#     # assert list(req) == {}


@pytest.mark.parametrize(('title', 'text'), ENTRIES)
def test_list_view(title, text, dbtransaction):
    """Test list view, which lists all entries."""
    # TODO: build dummy entries in fixture
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


@pytest.mark.parametrize(('title', 'text'), ENTRIES)
def test_entry_view(title, text, dbtransaction):
    """Test for entry view dictionary."""
    # TODO: build dummy entries in fixture
    # TODO: this test is repeating test_list_view
    entry = Entry(title=title, text=text)
    DBSession.add(entry)
    DBSession.flush()
    req = testing.DummyRequest()
    req.matchdict = {'id': entry.id}
    dic = single_entry_view(req)
    # TODO: test both attributes in one assert statement
    # NOTE: for attribute in [text, title] does not work
    assert dic['single_entry'].text == text
    assert dic['single_entry'].title == title
