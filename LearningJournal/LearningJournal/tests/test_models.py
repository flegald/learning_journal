
# _*_ coding:utf-8 _*_
"""Test models.py."""
import pytest
from .conftest import dbtransaction
from .conftest import DBSession
from ..models import Entry


def test_Entry(dbtransaction):
    """Test add Entry."""
    my_entry = Entry(title='test title', text='test txt')
    assert my_entry.id is None
    DBSession.add(my_entry)
    DBSession.flush()
    assert my_entry.id is not None
