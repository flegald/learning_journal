# column field datatypes
import datetime

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    String,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


# class MyModel(Base):
#     __tablename__ = 'models'
#     id = Column(Integer, primary_key=True)
#     name = Column(Text)
#     value = Column(Integer)

class Entry(Base):
    __tablename__ = 'Entry'
    id = Column(Integer, primary_key=True, )
    title = Column(String(128, convert_unicode=True),
                   nullable=False,
                   unique=True,
                   )
    text = Column(String(convert_unicode=True), nullable=False)
    created = Column(DateTime(timezone=False),
                     default=datetime.datetime.utcnow)

Index('my_index', Entry.title, unique=True, mysql_length=255)
