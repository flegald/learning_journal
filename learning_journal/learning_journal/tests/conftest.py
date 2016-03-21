# -*- coding: utf-8 -*-
import os
import pytest
from sqlalchemy import create_engine

from learning_journal.models import DBSession, Base
from ..models import Entry

TEST_DATABASE_URL = "postgres://David:saget@localhost:5432/testing"


@pytest.fixture(scope='session')
def sqlengine(request):
    engine = create_engine(TEST_DATABASE_URL)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    def teardown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture()
def dbtransaction(request, sqlengine):
    connection = sqlengine.connect()
    transaction = connection.begin()
    DBSession.configure(bind=connection)

    def teardown():
        transaction.rollback()
        connection.close()
        DBSession.remove()

    request.addfinalizer(teardown)

    return connection


@pytest.fixture()
def loaded_db(dbtransaction):
    my_entry = Entry(title="thefreshloaf", text="the text about fresh loaves")
    DBSession.add(my_entry)
    DBSession.flush()
    return DBSession
