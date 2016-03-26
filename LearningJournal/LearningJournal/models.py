
# column field datatypes
import datetime

from pyramid.security import (
    Allow,
    Everyone,
    )

from sqlalchemy import (
    Column,
    Index,
    Integer,
    DateTime,
    UnicodeText,
    Unicode,
    )

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class RootFactory(object):

    def __init__(self, request):
        pass

    __acl__ = [(Allow, Everyone, 'view'),
                (Allow, 'group:editors', 'edit')]


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True, )
    title = Column(Unicode(length=128),
                   nullable=False,
                   unique=True,
                   )
    text = Column(UnicodeText, nullable=False)
    created = Column(DateTime(timezone=False),
                     default=datetime.datetime.utcnow)
