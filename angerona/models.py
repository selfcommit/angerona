from sqlalchemy import (
    Column,
    LargeBinary,
    SmallInteger,
    String,
    DateTime
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Secret(Base):
    __tablename__ = 'secret'
    UniqHash = Column(String(64), primary_key=True)
    Nonce = Column(LargeBinary(32))
    Salt = Column(LargeBinary(32))
    Snippet = Column(String(8))
    ExpiryTime = Column(DateTime)
    LifetimeReads = Column(SmallInteger)
    CipherText = Column(LargeBinary(7680))

#Index('my_index', MyModel.name, unique=True, mysql_length=255)
