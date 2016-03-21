import pytest
from pyramid import testing
from .conftest import dbtransaction
from .conftest import DBSession
from ..views import (list_view, single_entry_view, add_entry_view, edit_entry_view)
from ..models import Entry


ENTRIES = [
    ('title 1', 'text 1'),
    ('title 2', 'text 2'),
]


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


# MultiDict was seen in AJ's tests, we do not understand it.

def test_add_entry_view_GET(dbtransaction):
    """Test for add entry view dictionary."""
    from pyramid.testing import DummyRequest
    from webob.multidict import MultiDict
    req = testing.DummyRequest()
    req.method = "GET"
    md = MultiDict()
    req.POST = md
    dic = add_entry_view(req)
    assert dic['form'].title is not None


def test_add_entry_view_POST(dbtransaction):
    """Test for add entry view dictionary."""
    from pyramid.testing import DummyRequest
    from webob.multidict import MultiDict
    req = testing.DummyRequest()
    req.method = "POST"
    md = MultiDict()
    md.add('title', 'test_title')
    req.POST = md
    dic = add_entry_view(req)
    assert dic['form'].title.data == 'test_title'


def test_edit_entry_view_GET(dbtransaction):
    """Test for edit entry view dictionary."""
    from pyramid.testing import DummyRequest
    from webob.multidict import MultiDict
    req = testing.DummyRequest()
    entry = Entry(title="test_title", text="test_text")
    DBSession.add(entry)
    DBSession.flush()
    req.method = "GET"
    req.matchdict = {'id': entry.id}
    md = MultiDict()
    req.POST = md
    dic = edit_entry_view(req)
    assert dic['form'].title.data == 'test_title'


def test_edit_entry_view_POST(dbtransaction):
    """Test for edit entry view dictionary."""
    from pyramid.testing import DummyRequest
    from webob.multidict import MultiDict
    req = testing.DummyRequest()
    req.method = "POST"
    md = MultiDict()
    entry = Entry(title="test_title", text="test_text")
    DBSession.add(entry)
    DBSession.flush()
    req.POST = md
    req.matchdict = {'id': entry.id}
    dic = edit_entry_view(req)
    assert dic['form'].title.data == 'test_title'
