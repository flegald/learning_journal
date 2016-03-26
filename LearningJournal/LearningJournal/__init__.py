"""Init."""
from pyramid.config import Configurator
import os
from sqlalchemy import engine_from_config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .security import groupfinder

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """Return a Pyramid WSGI application."""
    database_url = os.environ.get('DATABASE_URL', None)
    if database_url is not None:
        settings['sqlalchemy.url'] = database_url

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    # Security config
    authn_policy = AuthTktAuthenticationPolicy(
        'secret_string', callback=groupfinder, hashalg='sha512')

    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings, root_factory="LearningJournal.models.RootFactory")
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('single_entry', '/entries/{id}')
    config.add_route('add_entry', '/add_entry')
    config.add_route('edit_entry', '/edit_entry/{id}')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.scan()
    return config.make_wsgi_app()
