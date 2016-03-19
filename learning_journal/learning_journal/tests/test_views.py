import pytest
from pyramid import testing
from .conftest import dbtransaction
from .conftest import DBSession
from ..views import (list_view, single_entry_view)
from ..models import Entry


# def test_list(loaded_db):
#     return_dict = list_view(req)
#     print(return_dict['entries'].title)
#     # assert return_dict['entries'].title == "my_second_entry "
#     # assert list(req) == {}


def test_entry_view_text(dbtransaction):
    """Test for entry view dictionary text attribute."""
    new_model = Entry(title='thefreshloaf', text='text about fresh loaves')
    DBSession.add(new_model)
    DBSession.flush()
    test_request = testing.DummyRequest()
    test_request.matchdict = {'id': new_model.id}
    dic = list_view(test_request)
    print(dic['entries'])
    assert dic['entries'].id == 'text about fresh loaves'
