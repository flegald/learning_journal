# coding -*- utf-8 -*-
"""Test the login and access functionality."""
import pytest
from .conftest import dbtransaction
from pyramid import testing
import webtest
import os
from LearningJournal import main
from ..forms import EntryForm, LoginForm
from ..views import (
    list_view,
    single_entry_view,
    add_entry_view,
    edit_entry_view,
    login_view,
    logout_view
    )
from passlib.hash import sha512_crypt

GROUPS = {'david': ['group:editors']}
TESTDB = os.environ.get("TESTDB_URL")


ROUTES = [
    ('/'),
    ('/entries/1'),
    ('/add_entry'),
    ('/edit_entry/1'),
    ('/login'),
    ('/logout'),
]

RESTRICTED_ROUTES = [
    ('/add_entry'),
    ('/edit_entry/1'),
]

OPEN_ROUTES = [
    ('/'),
    ('/entries/2'),
    ('/entries/1')
]


@pytest.fixture()
def app():
    """Get for running app."""
    settings = {'sqlalchemy.url': TESTDB}
    app = main({}, **settings)
    return webtest.TestApp(app)


@pytest.fixture()
def auth_env():
    """Get Author environmental."""
    from learning_journal.security import check_pw
    os.environ['AUTH_PASSWORD'] = 'secret'


@pytest.fixture()
def authenticated_app(app, auth_env):
    """Get authenticated login."""
    data = {'username': 'david', 'password': os.environ.get('TEST_AUTH_PW', 'nothing')}
    app.post('/login', data)
    return app


def test_app_run(app):
    """Test app is running."""
    response = app.get('/entries/1')
    assert response


@pytest.mark.parametrize(('route'), RESTRICTED_ROUTES)
def test_login_fail(app, route):
    """Make sure user can access restricted pages."""
    response = app.get(route)
    assert 'Please Login' in response


@pytest.mark.parametrize(('route'), OPEN_ROUTES)
def test_all_access(app, route):
    """Test all users can see open pages."""
    response = app.get(route)
    assert "Please Login" not in response


def test_hash():
    """Test that passlib is encrypting."""
    test = sha512_crypt.encrypt('python')
    assert test != 'python'


@pytest.mark.parametrize(('route'), RESTRICTED_ROUTES)
def test_passing_login(authenticated_app, route):
    """Make sure login success works."""
    response = authenticated_app.get(route)
    assert "Please Login" not in response
